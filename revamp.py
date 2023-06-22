class BoardGame:
    def __init__(self):
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.players = ['W', 'B']
        self.turn = 0
        self.attack_option = False

    def place_piece(self, x, y, player):
        # Check if the spot is free and not adjacent to opponent's piece
        if self.board[x][y] != ' ':
            return False
        else:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if nx >= 0 and nx < 5 and ny >= 0 and ny < 5:
                        if self.board[nx][ny] == self.players[1 - self.players.index(player)]:
                            return False
            self.board[x][y] = player
            self.attack_option = True
            return True

    def attack_piece(self, x, y):
        if self.attack_option and self.board[x][y] != ' ':
            self.board[x][y] = ' '
            return True
        return False

    def print_board(self):
        print('  1 2 3 4 5')
        for idx, row in enumerate(self.board):
            print(chr(idx + ord('A')) + ' ' + '|'.join(row) + '|')

    def play_game(self):
        while self.turn < 25:
            player = self.players[self.turn % 2]
            self.print_board()
            action = input("Player {} turn. Choose action ('P' for place or 'A' for attack if available): ".format(player))
            if action.upper() == 'P':
                pos = input("Enter position to place piece (e.g., A1): ")
                x, y = ord(pos[0]) - ord('A'), int(pos[1:]) - 1
                if self.place_piece(x, y, player):
                    self.turn += 1
                else:
                    print("Invalid place move. Try again.")
            elif action.upper() == 'A' and self.attack_option:
                pos = input("Enter position to attack piece (e.g., A1): ")
                x, y = ord(pos[0]) - ord('A'), int(pos[1:]) - 1
                if self.attack_piece(x, y):
                    self.turn += 1
                else:
                    print("Invalid attack move. Try again.")
            else:
                print("Invalid action. Try again.")
        self.print_board()
        print("Game Over!")

if __name__ == "__main__":
    game = BoardGame()
    game.play_game()