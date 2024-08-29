import RPi.GPIO as GPIO
import threading
from time import sleep
from LED_management import start_animation, tie_animation, win_animation
import json
import random


import keyboard


class Game():
    button_pins = [20, 21, 27, 26,12,19]
    led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
    pvp_button = button_pins[0]
    pvc_button = button_pins[1]
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = 'X'


    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)
       
    def reset(self):
        for pin in self.led_pins:
            GPIO.output(pin, GPIO.LOW)
            self.board = ["", "", "", "", "", "", "", "", ""]

    def run(self):
        self.reset()
        self.update_board()
       
        start_animation()

        self.add_player_count()
        while True:
            if GPIO.input(self.pvp_button) == GPIO.HIGH:
                self.play_pvp()
                break
            elif GPIO.input(self.pvc_button) == GPIO.HIGH:
                self.play_pvc()
                break
           
            sleep(0.1)
       
       
    def check_buttons(self, test_with_terminal=False):
        buttons = [1,2,3,4,5,6,7,8,9]
        while True:
            if test_with_terminal:
               
                for button in buttons:
                    if keyboard.is_pressed(button):
                        self.current_button = self.button_pins[button-1]
                        print(f"Button {button} pressed.")
                        while keyboard.is_pressed(button):
                            pass
            else:
                for button in self.button_pins:
                    if GPIO.input(button) == GPIO.HIGH:
                        self.current_button = button
                       
                        while GPIO.input(button) == GPIO.HIGH:
                            sleep(0.1)
            sleep(0.1)



    def update_board(self):

        for i, symbol in enumerate(self.board):
            if symbol == 'X':
                self.turn_on(self.led_pins[i])
            elif symbol == 'O':
                thread = threading.Thread(target=self.show_O, args=(i,))
                thread.start()
                #self.threads.append(thread)
            else:
                self.turn_off(self.led_pins[i])

                   
           
    def turn_off(self, i):
        GPIO.output(i, GPIO.LOW)
       
    def turn_on(self, i):
        GPIO.output(i, GPIO.HIGH)

    def show_O(self, i):
        while self.board[i] == "O":
            self.turn_on(self.led_pins[i])
            sleep(0.2)
            self.turn_off(self.led_pins[i])
            sleep(0.2)

    def play_pvp(self):
        print('PVP')
        sleep(1)
        while True:
            valid_move = False
            while not valid_move:
                for i, button in enumerate(self.button_pins):
                    if GPIO.input(button) == GPIO.HIGH and self.board[i] == "":
                        self.board[i] = self.current_player
                        valid_move = True
                        break
                   
           
            self.update_board()
            if (result:= self.check_win_or_draw()) != False:
                self.end_game(result)
                break

            self.current_player = 'O' if self.current_player == 'X' else 'X'
           

    def check_win_or_draw(self):
        win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]]  
       
        for comb in win_combinations:
            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] != "":
                return self.board[comb[0]], comb
                   
        if all(tile != "" for tile in self.board):
            return 'Draw'

        return False

               
    def end_game(self, result):
        if result == 'Draw':
            print('Draw')
            #tie_animation
           
        else:
            player_won, comb = result[0], result[1]
            self.board = ["", "", "", "", "", "", "", "", ""]
            for i in comb:
                self.board[i] = player_won
            self.update_board()
            print('Player', player_won, 'won')
           
       
            sleep(3)
       
            #win_animation()

        self.run()



    def play_pvc(self):
        sleep(1)
       
        player_turn = random.choice([True, False])
        while True:
            valid_move = False
           
            if player_turn:
                while not valid_move:
                    for i, button in enumerate(self.button_pins):
                        if GPIO.input(button) == GPIO.HIGH and self.board[i] == "":
                            self.board[i] = self.current_player
                            valid_move = True
                            break
                       
            else:
                self.bot_move()
               
            self.update_board()
            if (result:= self.check_win_or_draw()) != False:
                self.end_game(result)
                break
           
            player_turn = not player_turn
            self.current_player = 'O' if self.current_player == 'X' else 'X'
       
       

    def bot_move():
        pass
       

       
   
   
   
   

    def add_player_count(self):
        filename = 'player_count.json'
   
        with open(filename, 'r') as file:
           
            data = json.load(file)
           
   
        if 'player_count' in data:
            data['player_count'] += 1
        else:
            data['player_count'] = 1
           
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
   


g = Game()
g.run()