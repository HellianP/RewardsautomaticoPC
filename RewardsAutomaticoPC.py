import pyautogui
import time
from pynput import keyboard

# Ativa FAILSAFE do PyAutoGUI (canto superior esquerdo encerra o programa)
pyautogui.FAILSAFE = True

# Flag para controle
parar = False

# Função chamada quando uma tecla é pressionada
def on_press(tecla):
    global parar
    try:
        if tecla == keyboard.Key.space:  # Se apertar espaço
            parar = True
            return False  # Para o listener parar
    except:
        pass

print("Posicione o mouse no local desejado em 5 segundos...")
time.sleep(5)

# Captura a posição inicial do mouse
x, y = pyautogui.position()
print(f"Posição capturada: x={x}, y={y}")

# Inicia o listener de teclado em paralelo
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Loop para digitar de 1 até 33
for numero in range(0, 30):  # Vai de 1 até 33
    if parar:  # Verifica se o usuário apertou espaço
        print("Programa interrompido pelo usuário (tecla espaço).")
        break

    # Clica na posição salva
    pyautogui.click(x, y)
    time.sleep(0.2)  # pequena pausa

    # Digita o número atual
    pyautogui.write(str(numero), interval=0.5)

    # Pressiona Enter
    pyautogui.press('enter')

    # Espera antes de apagar
    time.sleep(6)

print("Execução finalizada.")
