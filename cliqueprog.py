import tkinter as tk
from tkinter import messagebox, filedialog
import threading, time, json
import pyautogui
from pynput import mouse, keyboard
from datetime import datetime, timedelta

pyautogui.FAILSAFE = True

# Variáveis globais
recording = []
is_recording = False
record_start_time = None
stop_replay_flag = False

# ----- Captura de eventos -----
def on_move(x, y):
    if not is_recording:
        return
    t = time.time() - record_start_time
    recording.append({'type': 'move', 'time': t, 'x': x, 'y': y})

def on_click(x, y, button, pressed):
    if not is_recording:
        return
    t = time.time() - record_start_time
    recording.append({'type': 'click', 'time': t, 'x': x, 'y': y, 'button': str(button), 'pressed': pressed})

def on_press(key):
    if not is_recording:
        return
    t = time.time() - record_start_time
    recording.append({'type': 'key_press', 'time': t, 'key': str(key)})

def on_release(key):
    if not is_recording:
        return
    t = time.time() - record_start_time
    recording.append({'type': 'key_release', 'time': t, 'key': str(key)})

# ----- Gravação -----
def start_recording():
    global is_recording, record_start_time
    if is_recording:
        messagebox.showwarning("Aviso", "Já está gravando.")
        return
    messagebox.showinfo("Gravação", "A gravação começará em 5 segundos.")
    time.sleep(5)
    recording.clear()
    is_recording = True
    record_start_time = time.time()

    def record_thread():
        with mouse.Listener(on_move=on_move, on_click=on_click) as m_listener, \
             keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener:
            while is_recording:
                time.sleep(0.01)
            m_listener.stop()
            k_listener.stop()

    threading.Thread(target=record_thread, daemon=True).start()
    log_status("Gravando...")

def stop_recording():
    global is_recording
    if not is_recording:
        log_status("Nenhuma gravação ativa.")
        return
    is_recording = False
    log_status(f"Gravação encerrada ({len(recording)} eventos).")
    messagebox.showinfo("Gravação", f"{len(recording)} eventos gravados.")

# ----- Reprodução -----
def replay_events():
    global stop_replay_flag
    if not recording:
        messagebox.showwarning("Erro", "Nenhuma gravação disponível.")
        return
    stop_replay_flag = False
    log_status("Reproduzindo...")

    def stop_if_input_detected():
        """Monitoramento em paralelo: se houver movimento ou tecla, parar"""
        nonlocal_mouse = [None]
        def mouse_move_detected(x, y):
            global stop_replay_flag
            stop_replay_flag = True
            log_status("Reprodução interrompida por movimento do mouse.")
            return False

        def key_press_detected(key):
            global stop_replay_flag
            stop_replay_flag = True
            log_status("Reprodução interrompida por entrada do teclado.")
            return False

        with mouse.Listener(on_move=mouse_move_detected) as m_listener, \
             keyboard.Listener(on_press=key_press_detected) as k_listener:
            while not stop_replay_flag:
                time.sleep(0.1)
            m_listener.stop()
            k_listener.stop()

    threading.Thread(target=stop_if_input_detected, daemon=True).start()

    def play():
        prev_time = 0
        for ev in recording:
            if stop_replay_flag:
                break
            delay = ev['time'] - prev_time
            time.sleep(max(0, delay))
            prev_time = ev['time']
            try:
                if ev['type'] == 'move':
                    pyautogui.moveTo(ev['x'], ev['y'])
                elif ev['type'] == 'click' and ev['pressed']:
                    pyautogui.click(ev['x'], ev['y'])
                elif ev['type'] == 'key_press':
                    key = ev['key'].strip("'")
                    pyautogui.press(key)
            except Exception as e:
                log_status(f"Erro: {e}")
        log_status("Reprodução finalizada." if not stop_replay_flag else "Reprodução parada.")

    threading.Thread(target=play, daemon=True).start()

# ----- Agendamento -----
def schedule_replay():
    time_str = entry_time.get().strip()
    try:
        hh, mm = map(int, time_str.split(':'))
        now = datetime.now()
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)
        delay = (target - now).total_seconds()
        messagebox.showinfo("Agendado", f"Reprodução marcada para {target.strftime('%H:%M')}")
        threading.Thread(target=lambda: (time.sleep(delay), replay_events()), daemon=True).start()
        log_status(f"Agendado para {target.strftime('%H:%M:%S')}")
    except:
        messagebox.showerror("Erro", "Formato inválido. Use HH:MM.")

# ----- Salvamento -----
def save_recording():
    if not recording:
        messagebox.showwarning("Aviso", "Nenhum evento para salvar.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filepath:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(recording, f, indent=2, ensure_ascii=False)
        log_status(f"Gravação salva em {filepath}")

def load_recording():
    global recording
    filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            recording = json.load(f)
        log_status(f"{len(recording)} eventos carregados de {filepath}")

# ----- Interface Tkinter -----
def log_status(msg):
    text_status.config(state='normal')
    text_status.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    text_status.see('end')
    text_status.config(state='disabled')

root = tk.Tk()
root.title("Gravador e Reprodutor Automático")
root.geometry("460x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Agendar reprodução (HH:MM):").pack()
entry_time = tk.Entry(frame, width=10, justify='center')
entry_time.pack(pady=3)

tk.Button(frame, text="Iniciar gravação", width=20, command=lambda: threading.Thread(target=start_recording).start()).pack(pady=3)
tk.Button(frame, text="Parar gravação", width=20, command=stop_recording).pack(pady=3)
tk.Button(frame, text="Reproduzir agora", width=20, command=replay_events).pack(pady=3)
tk.Button(frame, text="Agendar reprodução", width=20, command=schedule_replay).pack(pady=3)
tk.Button(frame, text="Salvar gravação", width=20, command=save_recording).pack(pady=3)
tk.Button(frame, text="Carregar gravação", width=20, command=load_recording).pack(pady=3)

text_status = tk.Text(root, height=10, state='disabled', wrap='word')
text_status.pack(fill='both', padx=10, pady=10)

root.mainloop()




oloco bixo
