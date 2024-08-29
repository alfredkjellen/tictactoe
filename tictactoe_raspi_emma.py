import RPi.GPIO as GPIO
import threading
from time import sleep
from räknar_spelare import lägg_till_spelare, hämta_nuvarande_antal
from LED_management import start_animation, win_animation, tie_animation

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

button_pins = [27, 21, 20, 26, 12, 19]
led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
board = ["", "", "", "", "", "", "", "", ""]
threads = []
turn = 'X'
spelet_spelas = True

for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def turn_on(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def reset_board():
    global board
    board = ["", "", "", "", "", "", "", "", ""]
    for pin in led_pins:
        turn_off(pin)
        
def show_X(position):
    turn_on(led_pins[position])

def show_O(position):
    while spelet_spelas:
        if board[position] == "O":
            turn_on(led_pins[position])
            sleep(0.5)
            turn_off(led_pins[position])
            sleep(0.5)
        else: 
            break
        
def switch_turn():
    global turn
    if turn == 'X':
        turn = 'O'
        
    elif turn == 'O':
        turn = 'X'

def update_board():
    global threads
    print(board)
    for i, state in enumerate(board):
        if state == "X":
            show_X(i)
        elif state == "O":
            thread = threading.Thread(target=show_O, args=(i,))
            thread.start()
            threads.append(thread)
        else:
            turn_off(led_pins[i])
    for thread in threads:
        thread.join()
    threads.clear()

            
        


def check_buttons():
    global spelet_spelas
    while spelet_spelas:
        for i in range(len(button_pins)):
            if GPIO.input(button_pins[i]) == GPIO.HIGH:
                if board[i] == '':
                    board[i] = turn
                    update_board()
                    if check_win():
                        win_animation()
                        reset_board()
                        spelet_spelas = False
                    elif '' not in board:
                        tie_animation()
                        reset_board()
                        spelet_spelas = False
                    switch_turn()
                    sleep(0.5)

        
def check_win():
    for x in range (0, 7, 3):
        if board[x] == board[x + 1] == board[x + 2] and board[x] != '':
            return True

    for x in range (3):
        if board[x] == board[x + 3] == board[x + 6] and board[x] != '':
            return True

    for x in range (2, 5, 2):
        if board[4 - x] == board[x] == board[4 + x] and board[x] != '':
            return True
    return False
            
def run():
    global spelet_spelas
    spelet_spelas = True
    start_animation()
    lägg_till_spelare()
    hämta_nuvarande_antal()
    check_buttons()
    run()
    
    
run()