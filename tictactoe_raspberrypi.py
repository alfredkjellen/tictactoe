import RPi.GPIO as GPIO
import threading
from time import sleep

#for testing
import keyboard


class Game():
    button_pins = [27, 21, 20]
    led_pins = [2, 3, 4, 7, 6, 5, 8, 9, 10]
    pvp_button = button_pins[0]
    pvc_button = button_pins[1]
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = 'X'

    threads = []

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
        while True:
            if GPIO.input(self.pvp_button) == GPIO.HIGH:
                self.play_pvp
                break
            elif GPIO.input(self.pvc_button) == GPIO.HIGH:
                self.play_pvc
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
                self.threads.append(thread)
            else:
                self.turn_off(self.led_pins[i])

                    
            
    def turn_off(i):
        GPIO.output(i, GPIO.LOW)
        
    def turn_on(i):
        GPIO.output(i, GPIO.HIGH)

    def show_O(self, i):
        while self.board[i] == "O":
            self.turn_on(self.led_pins[i])
            sleep(0.2)
            self.turn_off(self.led_pins[i])
            sleep(0.2)

    def play_pvp(self):
        while True:
            while True:
                for i, button in enumerate(self.button_pins):
                    if GPIO.input(button) == GPIO.HIGH:
                        move = i

                if self.board[move] == "":
                    self.board[move] = self.current_player
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
        else:
            player_won, comb = result[0], result[1]
            self.board = ["", "", "", "", "", "", "", "", ""]
            for i in comb:
                self.board[i] = player_won
            self.update_board()
            print('Player', player_won, 'won')
        
        sleep(3)


        self.run()



    def play_pvc():
        pass




        





        
        

        


    