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

# Calcula tempo total estimado (6.7 segundos por iteração)
tempo_total = 33 * 6.7  # 6.7 segundos é aproximadamente o tempo de cada ciclo

# Loop para digitar de 0 até 33
for numero in range(0, 33):
    if parar:
        print("Programa interrompido pelo usuário (tecla espaço).")
        break

    # Calcula tempo restante
    tempo_restante = (33 - numero) * 6.7
    minutos = int(tempo_restante // 60)
    segundos = int(tempo_restante % 60)
    
    print(f"Número atual: {numero}/33 - Tempo restante estimado: {minutos}m {segundos}s")

    pyautogui.click(x, y)
    time.sleep(0.2)

    pyautogui.write(str(numero), interval=0.5)
    pyautogui.press('enter')
    time.sleep(6)

print("Execução finalizada.")
