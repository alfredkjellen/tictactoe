import RPi.GPIO as GPIO
import threading
from time import sleep
from räknar_spelare import lägg_till_spelare, hämta_nuvarande_antal

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

turn = 'X'

button_pins = [27, 21, 20]
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
board = ["", "", "", "", "", "", "", "", ""]
threads = []


def switch_turn():
    global turn
    if turn == 'X':
        turn = 'O'
        
    elif turn == 'O':
        turn = 'X'

for pin in button_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def turn_on(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def reset():
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)
        
def show_X(position):
    turn_on(led_pins[position])

def show_O(position):
    while board[position] == "O":
        turn_on(led_pins[position])
        sleep(0.5)
        turn_off(led_pins[position])
        sleep(0.5)
        
def update_board():
    global board
    print(board)
    threads = []
    for i, state in enumerate(board):
        if state == "X":
            show_X(i)
        elif state == "O":
            thread = threading.Thread(target=show_O, args=(i,))
            thread.start()
            threads.append(thread)
            
        else:
            turn_off(led_pins[i])
            
        


def check_buttons():
    global board
    while True:
        for i in range(len(button_pins)):
            if GPIO.input(button_pins[i]) == GPIO.HIGH:
                board[i] = turn
                update_board()
                
                switch_turn()
                sleep(0.5)
                
        
    
        
                
            
def run():
    global threads
    thread1 = threading.Thread(target=check_buttons)
    #thread2 = threading.Thread(target=update_board)
    threads.append(thread1)
    #threads.append(thread2)
    
    thread1.start()
    #thread2.start()
    
    
run()