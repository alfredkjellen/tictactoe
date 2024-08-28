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
    current_button = None

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
        thread1 = threading.Thread(target=self.check_buttons,args=(True,)).start()
        thread2 = threading.Thread(target=self.handle_game).start()
        self.threads.append(thread1)
        self.threads.append(thread2)
        
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
                        while button == GPIO.HIGH:
                            pass


    def handle_game(self):
        while True:
            if self.current_button == self.pvp_button:
                self.current_button = None
                self.play_pvp()
                break

            elif self.current_button == self.pvc_button:
                self.current_button = None
                self.play_pvc()
                break

    def update_board(self):
        for i, symbol in enumerate(self.board):
            if symbol == 'X':
                self.turn_on(i)
            elif symbol == 'O':
                thread = threading.Thread(target=self.show_O, args=(i,))
                thread.start()
                self.threads.append(thread)
            else:
                self.turn_off(i)               
        
    def turn_off(led_pin):
        GPIO.output(led_pin, GPIO.LOW)
        
    def turn_on(led_pin):
        GPIO.output(led_pin, GPIO.HIGH)

    def show_O(self, i):
        while self.board[i] == "O":
            self.turn_on(self.led_pins[i])
            sleep(0.2)
            self.turn_off(self.led_pins[i])
            sleep(0.2)


    def play_pvp(self):
        while True:

            while True:
                move = self.current_button
                self.current_button = None
                if self.board[move] == "":
                    break
            
            self.board[move] = self.current_player
            self.update_board()

            if result:= self.check_win_or_draw() is not False:
                self.end_game(result)
                break

            self.current_player = 'O' if self.current_button == 'X' else 'X'

            

    def check_win_or_draw(self):
        win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], 
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]]  
        
        for comb in win_combinations:
            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] != "":
                return self.board[comb[0]], comb
        
        if all(self.board) != "":
            return 'Draw'

        return False

                
    def end_game(self, result):
        if result == 'Draw':
            print('Draw')
        else:
            player_won, comb = result
            self.board = ["", "", "", "", "", "", "", "", ""]
            for i in comb:
                self.board[i] = player_won
            self.update_board()
        
        sleep(3)

        for thread in self.threads:
            thread.join()

        self.run()



    def play_pvc():
        pass


        





        
        

        


    