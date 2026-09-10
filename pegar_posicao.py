import pyautogui
import time

time.sleep(3)


# Pega a posição atual do mouse (retorna uma tupla x, y)
posicao_atual = pyautogui.position()

print(posicao_atual)