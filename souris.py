import pyautogui
import time

def bouger_et_cliquer(intervalle=60):
    print("Script actif. Ctrl+C pour arrêter.")
    try:
        while True:
            x, y = pyautogui.position()  # position actuelle
            pyautogui.moveTo(x + 15, y, duration=0.1)
            pyautogui.click()
            pyautogui.moveTo(x, y, duration=0.1)
            time.sleep(intervalle)
    except KeyboardInterrupt:
        print("Script arrêté.")

bouger_et_cliquer(intervalle=10)
