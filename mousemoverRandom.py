import pyautogui
import time
import random
import threading
from datetime import datetime

# Zorg ervoor dat je pyautogui hebt geïnstalleerd:
# pip install pyautogui

class RandomMouseMover:
    def __init__(self):
        self._running = False
        self._thread = None

    def _move_mouse(self):
        while self._running:
            try:
                x_offset = 0
                y_offset = 0
                if random.choice([True, False]):  # Kies willekeurig x of y
                    x_offset = random.choice([-10, 10])
                else:
                    y_offset = random.choice([-10, 10])

                current_x, current_y = pyautogui.position()
                pyautogui.moveRel(x_offset, y_offset, duration=0.25)  # Beweeg relatief met een korte animatie
                time.sleep(300)  # Wacht 5 minuten (300 seconden)
            except Exception as e:
                print(f"Er is een fout opgetreden in de muisbeweging: {e}")
                self.stop()

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._move_mouse)
            self._thread.daemon = True  # Zorgt ervoor dat de thread stopt als het hoofdprogramma stopt
            self._thread.start()
            print("De willekeurige muisbeweging is gestart.")
        else:
            print("De willekeurige muisbeweging is al gestart.")

    def stop(self):
        if self._running:
            self._running = False
            if self._thread and self._thread.is_alive():
                self._thread.join()  # Wacht tot de thread is gestopt
            print("De willekeurige muisbeweging is gestopt.")
        else:
            print("De willekeurige muisbeweging is al gestopt.")

if __name__ == "__main__":
    # Voorbeeld van hoe je de klasse kunt gebruiken
    mouse_mover = RandomMouseMover()

    try:
        mouse_mover.start()
        input("Druk op Enter om de muisbeweging te stoppen...\n")
    finally:
        mouse_mover.stop()
        print("Het programma is afgesloten.")
