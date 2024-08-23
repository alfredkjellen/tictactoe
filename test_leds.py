import RPi.GPIO as GPIO
import threading
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

board = ["", "", "", "", "", "", "", "", ""]


def show_X(position):
    GPIO.output(pins[position], GPIO.HIGH)

def show_O(position):
    while board[position] == "O":
        GPIO.output(pins[position], GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pins[position], GPIO.LOW)
        time.sleep(0.5)

def update_board():
    threads = []
    for i, state in enumerate(board):
        if state == "X":
            show_X(i)
        elif state == "O":
            thread = threading.Thread(target=show_O, args=(i,))
            thread.start()
            threads.append(thread)
        else:
            GPIO.output(pins[i], GPIO.LOW)

    for thread in threads:
        thread.join()


board = ["X", "O", "", "X", "", "O", "", "", "X"]
update_board()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
