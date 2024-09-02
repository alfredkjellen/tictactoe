import RPi.GPIO as GPIO
import threading
from time import sleep
from LED_management import start_animation, tie_animation, end_animation
import json
import random

class Game():
    #constants
    BUTTON_PINS = [21, 20, 16, 12, 7, 8, 25, 24, 23]
    LED_PINS = [2, 3, 4, 17, 27, 22, 10, 9, 11]
    TIME_BETWEEN_BLINKS = 0.2
    TIME_BEFORE_BOT_MOVE = 0.9
    TIME_SHOW_WIN_ANIMATION = 2.5
    PVP_BUTTON = BUTTON_PINS[4]
    PVC_BUTTON = BUTTON_PINS[3]
   
    #game data
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = 'X'
    game_is_running = False    

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.BUTTON_PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for pin in self.LED_PINS:
            GPIO.setup(pin, GPIO.OUT)
       
    def reset(self):
        for pin in self.LED_PINS:
            GPIO.output(pin, GPIO.LOW)
            self.board = ["", "", "", "", "", "", "", "", ""]

    def run(self):
        self.reset()
        self.add_player_count()
       
        thread_animation = threading.Thread(target=start_animation).start()

        while True:
            if GPIO.input(self.PVP_BUTTON) == GPIO.HIGH:
                end_animation()
                self.game_is_running = True
                thread_x = threading.Thread(target=self.show_X).start()
                thread_o = threading.Thread(target=self.show_O).start()
                self.play_pvp()
                break
            elif GPIO.input(self.PVC_BUTTON) == GPIO.HIGH:
                end_animation()
                self.game_is_running = True
                thread_x = threading.Thread(target=self.show_X).start()
                thread_o = threading.Thread(target=self.show_O).start()
                self.play_pvc()
                break
           
           
    def turn_off(self, i):
        GPIO.output(i, GPIO.LOW)
       
    def turn_on(self, i):
        GPIO.output(i, GPIO.HIGH)


    def show_X(self):
        while self.game_is_running:
            for i, symbol in enumerate(self.board):
                if symbol == "X":
                    self.turn_on(self.LED_PINS[i])
                elif symbol == "":
                    self.turn_off(self.LED_PINS[i])

    def show_O(self):
        while self.game_is_running:
            o_list = []
           
            for i, symbol in enumerate(self.board):
                if symbol == "O":
                    o_list.append(i)
            for i in o_list:
                self.turn_on(self.LED_PINS[i])
            sleep(0.2)
            for i in o_list:
                self.turn_off(self.LED_PINS[i])
            sleep(0.2)
                   

    def play_pvp(self):
        print('PVP')
        sleep(1.5)
        while True:
            valid_move = False
            while not valid_move:
                for i, button in enumerate(self.BUTTON_PINS):
                    if GPIO.input(button) == GPIO.HIGH and self.board[i] == "":
                        self.board[i] = self.current_player
                        valid_move = True
                        break
                   
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
            sleep(2)
            self.board = ["", "", "", "", "", "", "", "", ""]
            self.game_is_running = False
            tie_animation()
           
        else:
            sleep(2)
            player_won, comb = result[0], result[1]
            self.board = ["", "", "", "", "", "", "", "", ""]
            sleep(0.1)
            for i in comb:
                self.board[i] = player_won
           
            print('Player', player_won, 'won')
           
            sleep(2.5)
            self.game_is_running = False
           

        self.run()



    def play_pvc(self):
        print('PVC')
        sleep(1)
        player_turn = random.choice([True, False])
        while True:
            valid_move = False
           
            if player_turn:
                while not valid_move:
                    for i, button in enumerate(self.BUTTON_PINS):
                        if GPIO.input(button) == GPIO.HIGH and self.board[i] == "":
                            self.board[i] = self.current_player
                            valid_move = True
                            break
                       
            else:
                sleep(1)
                self.bot_move()
               
           
            if (result:= self.check_win_or_draw()) != False:
                self.end_game(result)
                break
           
            player_turn = not player_turn
            self.current_player = 'O' if self.current_player == 'X' else 'X'
       
       
       

    def bot_move(self):
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]
           
        def center_strategy():
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.current_player
                    if self.check_win_or_draw():
                        return
                    self.board[i] = ""
                   
            opponent = 'O' if self.current_player == 'X' else 'X'
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = opponent
                    if self.check_win_or_draw():
                        self.board[i] = self.current_player
                        return
                    self.board[i] = ""

           
           
            if self.board[4] == "":
                self.board[4] = self.current_player
                return
           
            random.shuffle(corners)
            for i in corners:
                if self.board[i] == "":
                    self.board[i] = self.current_player
                    return

           
            random.shuffle(edges)
            for i in edges:
                if self.board[i] == "":
                    self.board[i] = self.current_player
                    return
       
        center_strategy()


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