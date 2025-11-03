import tkinter as tk
from tkinter import messagebox
import time
import threading
import pyautogui
from pynput import keyboard

pyautogui.FAILSAFE = True
parar = False
posicao_mouse = None

def capturar_posicao():
    global posicao_mouse
    messagebox.showinfo("Posicionamento", "Coloque o mouse no local desejado e aguarde 5 segundos.")
    time.sleep(5)
    posicao_mouse = pyautogui.position()
    lbl_posicao.config(text=f"Posição capturada: {posicao_mouse}")
    
def parar_execucao():
    global parar
    parar = True
    
def iniciar():
    global parar, posicao_mouse
    parar = False

    if posicao_mouse is None:
        messagebox.showwarning("Erro", "Capture a posição do mouse primeiro!")
        return

    try:
        inicio = int(entry_inicio.get())
        fim = int(entry_fim.get())
        delay = float(entry_delay.get())
    except:
        messagebox.showwarning("Erro", "Verifique os valores inseridos.")
        return

    thread = threading.Thread(target=executar, args=(inicio, fim, delay))
    thread.start()

def executar(inicio, fim, delay):
    global parar

    total = (fim - inicio + 1)
    tempo_total = total * delay

    for i, numero in enumerate(range(inicio, fim + 1)):
        if parar:
            lbl_status.config(text="Status: Interrompido")
            return
        
        tempo_restante = tempo_total - (i * delay)
        minutos = int(tempo_restante // 60)
        segundos = int(tempo_restante % 60)

        lbl_status.config(text=f"Enviando: {numero}/{fim} | Restante: {minutos}m {segundos}s")

        x, y = posicao_mouse
        pyautogui.click(x, y)
        time.sleep(0.2)

        pyautogui.write(str(numero), interval=0.05)
        pyautogui.press('enter')
        time.sleep(delay)

    lbl_status.config(text="Finalizado!")

# Interface
root = tk.Tk()
root.title("Automação de Envio")

tk.Label(root, text="Início:").grid(row=0, column=0)
entry_inicio = tk.Entry(root)
entry_inicio.grid(row=0, column=1)
entry_inicio.insert(0, "0")

tk.Label(root, text="Fim:").grid(row=1, column=0)
entry_fim = tk.Entry(root)
entry_fim.grid(row=1, column=1)
entry_fim.insert(0, "33")

tk.Label(root, text="Delay (s):").grid(row=2, column=0)
entry_delay = tk.Entry(root)
entry_delay.grid(row=2, column=1)
entry_delay.insert(0, "6.7")

btn_posicao = tk.Button(root, text="Capturar posição do mouse", command=capturar_posicao)
btn_posicao.grid(row=3, column=0, columnspan=2)

lbl_posicao = tk.Label(root, text="Posição não capturada")
lbl_posicao.grid(row=4, column=0, columnspan=2)

btn_iniciar = tk.Button(root, text="Iniciar", bg="green", fg="white", command=iniciar)
btn_iniciar.grid(row=5, column=0)

btn_parar = tk.Button(root, text="Parar", bg="red", fg="white", command=parar_execucao)
btn_parar.grid(row=5, column=1)

lbl_status = tk.Label(root, text="Status: Aguardando")
lbl_status.grid(row=6, column=0, columnspan=2)

root.mainloop()


                      
 