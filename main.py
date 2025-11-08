from tkinter import *
import numpy as np
from ai.ai_easy import AIEasy

size_of_board = 600
symbol_size = (size_of_board / 15 - size_of_board / 30) / 2
symbol_thickness = 3
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.ai = AIEasy('O')
        self.board_status = np.zeros(shape=(15, 15))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(14):
            self.canvas.create_line((i + 1) * size_of_board / 15, 0, (i + 1) * size_of_board / 15, size_of_board)

        for i in range(14):
            self.canvas.create_line(0, (i + 1) * size_of_board / 15, size_of_board, (i + 1) * size_of_board / 15)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = True
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(15, 15))

        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 8, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 15) * logical_position + size_of_board / 30

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 15), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        n = 15  
        win_len = 5    # số quân cần để thắng (5 liên tiếp)

        # Duyệt từng ô trên bàn cờ
        for r in range(n):
            for c in range(n):
                player = self.board_status[r][c]
                if player == 0 or player is None:
                    continue  # bỏ qua ô trống

                # 1️⃣ Kiểm tra hàng ngang →
                if c + win_len <= n and all(self.board_status[r][c + k] == player for k in range(win_len)):
                    return player

                # 2️⃣ Kiểm tra cột dọc ↓
                if r + win_len <= n and all(self.board_status[r + k][c] == player for k in range(win_len)):
                    return player

                # 3️⃣ Kiểm tra chéo chính ↘
                if r + win_len <= n and c + win_len <= n and all(self.board_status[r + k][c + k] == player for k in range(win_len)):
                    return player

                # 4️⃣ Kiểm tra chéo phụ ↙
                if r + win_len <= n and c - win_len + 1 >= 0 and all(self.board_status[r + k][c - k] == player for k in range(win_len)):
                    return player

        # Nếu duyệt hết mà không ai thắng
        return None



    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover

    def click(self, event):
        if self.reset_board:
            # Nếu ván cũ đã kết thúc → bấm để chơi lại
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
            return

        # Nếu người chơi X click
        if self.player_X_turns:
            grid_position = [event.x, event.y]
            logical_position = self.convert_grid_to_logical_position(grid_position)

            if not self.is_grid_occupied(logical_position):
                # Người chơi đi X
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.player_X_turns = False  # chuyển lượt cho AI

                # Kiểm tra nếu người chơi vừa thắng
                if self.is_gameover():
                    self.display_gameover()
                    return

            # Lượt của AI
            ai_move = self.ai.choose_move(self.board_status)
            if ai_move is not None and not self.is_grid_occupied(ai_move):
                self.draw_O(ai_move)
                self.board_status[ai_move[0]][ai_move[1]] = 1
                self.player_X_turns = True  # quay lại lượt người chơi

                # Kiểm tra nếu AI thắng hoặc hòa
                if self.is_gameover():
                    self.display_gameover()

game_instance = Tic_Tac_Toe()
game_instance.mainloop()