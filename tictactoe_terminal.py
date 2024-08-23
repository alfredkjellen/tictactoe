import random

class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def display(self):
        print('-'* 9)
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)

        print('')

    def update(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        
        return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != ' ':
            return self.board[2][0]
        return None

    def is_full(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))
    
    def __getitem__(self, cor):
        row, col = cor
        return self.board[row][col]

    def __setitem__(self, cor, value):
        row, col = cor
        self.board[row][col] = value

class Game:
    
    pos_map = {'q': (0, 0), 'w': (0, 1), 'e': (0, 2),
    'a': (1, 0), 's': (1, 1), 'd': (1, 2),
    'z': (2, 0), 'x': (2, 1), 'c': (2, 2)}

    def __init__(self):
        self.board = Board()
        self.game_modes = ['PvC', 'PvP']
        self.current_player = 'X'
        self.game_mode = self.choose_game_mode()


    def choose_game_mode(self):
        while True:
            try:
                index = int(input("Choose game mode.\nEnter 1 if you want to play vs the computer \nEnter 2 if you want to play vs another player ").strip()) - 1
                return self.game_modes[index]
            except: 
                print("Wrong input. Press'1' or '2'.")

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'


    def get_player_move(self):
        while True:

            try:
                pos = input(f"Player {self.current_player}, enter your move Q W E, A S D, Z X C: ").strip().lower()
                row, col = self.pos_map[pos]
                if self.board.update(row, col, self.current_player):
                    break
                else:
                    print('Occupied')
            except:
                print("Wrong input")


    def get_bot_move(self):

        bot = 'O' if self.current_player == 'X' else 'X'

        def check_for_win_or_block(player):
            for row in range(3):
                if self.board[row, 0] == self.board[row, 1] == player and self.board[row, 2] == ' ':
                    return (row, 2)
                if self.board[row, 1] == self.board[row, 2] == player and self.board[row, 0] == ' ':
                    return (row, 0)
                if self.board[row, 0] == self.board[row, 2] == player and self.board[row, 1] == ' ':
                    return (row, 1)
            for col in range(3):
                if self.board[0, col] == self.board[1, col] == player and self.board[2, col] == ' ':
                    return (2, col)
                if self.board[1, col] == self.board[2, col] == player and self.board[0, col] == ' ':
                    return (0, col)
                if self.board[0, col] == self.board[2, col] == player and self.board[1, col] == ' ':
                    return (1, col)
            if self.board[0, 0] == self.board[1, 1] == player and self.board[2, 2] == ' ':
                return (2, 2)
            if self.board[1, 1] == self.board[2, 2] == player and self.board[0, 0] == ' ':
                return (0, 0)
            if self.board[0, 2] == self.board[1, 1] == player and self.board[2, 0] == ' ':
                return (2, 0)
            if self.board[1, 1] == self.board[2, 0] == player and self.board[0, 2] == ' ':
                return (0, 2)
            return None


        def choose_corner():
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for corner in corners:
                if self.board[corner[0], corner[1]] == ' ':
                    return corner
            return None

        def choose_side():
            sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
            for side in sides:
                if self.board[side[0], side[1]] == ' ':
                    return side
            return None

        move = check_for_win_or_block(bot)
        if move:
            self.board.update(move[0], move[1], bot)
            return
        
        move = check_for_win_or_block(self.current_player)
        if move:
            self.board.update(move[0], move[1], bot)
            return
        

        if self.board[1, 1] == ' ':
            self.board.update(1, 1, bot)
            return
    
        move = choose_corner()
        if move:
            self.board.update(move[0], move[1], bot)
            return
        
        move = choose_side()
        if move:
            self.board.update(move[0], move[1], bot)
            return
        
        empty_positions = [(row, col) for row in range(3) for col in range(3) if self.board[row, col] == ' ']
        move = random.choice(empty_positions)
        self.board.update(move[0], move[1], bot)


    def play_pvp(self):
        while True:
            self.board.display()
            self.get_player_move()

            winner = self.board.check_winner()
            if winner:
                self.board.display()
                print(f"Player {winner} wins!")
                break
            elif self.board.is_full():
                self.board.display()
                print("Draw!")
                break

            self.switch_player()



    def play_pvc(self):

        while True:
            try:
                user_input = input('If you want to start, press 1. \nElse press enter ')
                you_start = True if user_input == '1' else False
            except:
                print('Wrong input')

            else:
                break
    
        while True:
            self.board.display()

            if you_start:
                self.get_player_move()
            else:
                self.get_bot_move()

            winner = self.board.check_winner()
            you_start = not you_start

            if winner:
                self.board.display()
                print(f"Player {winner} wins!")
                break
            elif self.board.is_full():
                self.board.display()
                print("Draw!")
                break

    def play(self):
        if self.game_mode == 'PvP':
            self.play_pvp()
        else:
            self.play_pvc()

game = Game()
game.play()
#hej