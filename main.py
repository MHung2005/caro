# ...existing code...
from tkinter import *
import threading
import numpy as np
from ai.ai_easy import AIEasy
from ai.ai_minimax import AIMinimax
from ai.ai_hard import AIHard

size_of_board = 600
symbol_size = (size_of_board / 10 - size_of_board / 30) / 2
symbol_thickness = 3
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'
num_board = 10


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')

        # Control: chọn mức AI (chỉ có Human vs AI)
        control_frame = Frame(self.window)
        control_frame.pack(pady=6, anchor='w')

        Label(control_frame, text="Chế độ: ").pack(side=LEFT, padx=(0,8))

        self.ai_level_var = StringVar(value="Hard")  # mặc định Hard
        rb_easy = Radiobutton(control_frame, text="Easy", variable=self.ai_level_var, value="Easy", command=self.change_ai_level)
        rb_easy.pack(side=LEFT)
        rb_minimax = Radiobutton(control_frame, text="Minimax", variable=self.ai_level_var, value="Minimax", command=self.change_ai_level)
        rb_minimax.pack(side=LEFT)
        rb_alphabeta = Radiobutton(control_frame, text="alpha-beta", variable=self.ai_level_var, value="alpha-beta", command=self.change_ai_level)
        rb_alphabeta.pack(side=LEFT)

        new_btn = Button(control_frame, text='New Game', command=self.play_again)
        new_btn.pack(side=LEFT, padx=8)

        # Canvas và binding click
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True

        # Tạo instance AI cho 2 mức
        # AIEasy constructor yêu cầu symbol — truyền 1 (O)
        self.ai_easy = AIEasy(1)
        self.ai_minimax = AIMinimax()
        self.ai_alpha_beta = AIHard(ai_player=1, max_depth=2)

        # self.ai trỏ tới instance hiện tại (mặc định Hard)
        self.ai = self.ai_alpha_beta

        self.board_status = np.zeros(shape=(num_board, num_board))

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

    def change_ai_level(self):
        if self.ai_level_var.get() == "Easy":
            self.ai = self.ai_easy
        if self.ai_level_var.get() == "Minimax":
            self.ai = self.ai_minimax
        if self.ai_level_var.get() == "alpha-beta":
            self.ai = self.ai_alpha_beta


    def initialize_board(self):
        for i in range(num_board - 1):
            self.canvas.create_line((i + 1) * size_of_board / num_board, 0, (i + 1) * size_of_board / num_board, size_of_board)

        for i in range(num_board - 1):
            self.canvas.create_line(0, (i + 1) * size_of_board / num_board, size_of_board, (i + 1) * size_of_board / num_board)

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.player_X_starts = True
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(num_board, num_board))

        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

    # ------------------------------------------------------------------
    # Drawing Functions:
    # ------------------------------------------------------------------
    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
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
    # ------------------------------------------------------------------
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / num_board) * logical_position + size_of_board / (num_board*2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / num_board), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player_val):

        n = 10
        win_len = 5

        for r in range(n):
            for c in range(n):
                if self.board_status[r][c] != player_val:
                    continue
                if player_val == 0 or player_val is None:
                    continue

                if c + win_len <= n and all(self.board_status[r][c + k] == player_val for k in range(win_len)):
                    return player_val

                if r + win_len <= n and all(self.board_status[r + k][c] == player_val for k in range(win_len)):
                    return player_val

                if r + win_len <= n and c + win_len <= n and all(self.board_status[r + k][c + k] == player_val for k in range(win_len)):
                    return player_val

                if r + win_len <= n and c - win_len + 1 >= 0 and all(self.board_status[r + k][c - k] == player_val for k in range(win_len)):
                    return player_val

        return None

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True
        return tie

    def is_gameover(self):
        self.X_wins = self.is_winner(-1)
        if not self.X_wins:
            self.O_wins = self.is_winner(1)

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
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
            return

        # Luôn là Human (X) click; chỉ cho phép click khi đến lượt X
        if not self.player_X_turns:
            return

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

            # Tính toán nước đi AI trên thread nền
            def compute_ai_move(board_snapshot, ai_instance):
                ai_move = ai_instance.choose_move(board_snapshot)
                def apply_move():
                    if ai_move is not None and not self.is_grid_occupied(ai_move):
                        self.draw_O(ai_move)
                        self.board_status[ai_move[0]][ai_move[1]] = 1
                        self.player_X_turns = True
                        if self.is_gameover():
                            self.display_gameover()
                self.window.after(0, apply_move)

            board_copy = np.array(self.board_status, copy=True)
            threading.Thread(target=compute_ai_move, args=(board_copy, self.ai), daemon=True).start()

game_instance = Tic_Tac_Toe()
game_instance.mainloop()