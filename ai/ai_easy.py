import random

class AIEasy:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def choose_move(self, board_status):
        empty_cells = [
            (r, c) for r in range(15)
            for c in range(15)
            if board_status[r][c] == 0
        ]
        return random.choice(empty_cells)

#  # Lượt của AI — tính toán trong thread để không block GUI
#             def compute_ai_move(board_snapshot):
#                 ai_move = self.ai.choose_move(board_snapshot)
#                 def apply_move():
#                     if ai_move is not None and not self.is_grid_occupied(ai_move):
#                         self.draw_O(ai_move)
#                         self.board_status[ai_move[0]][ai_move[1]] = 1
#                         self.player_X_turns = True
#                         if self.is_gameover():
#                             self.display_gameover()
#                 # schedule apply_move on main thread
#                 self.window.after(0, apply_move)

#             # truyền bản sao của board để tránh race và mutation
#             board_copy = np.array(self.board_status, copy=True)
#             threading.Thread(target=compute_ai_move, args=(board_copy,), daemon=True).start()

# size_of_board = 600
# symbol_size = (size_of_board / 15 - size_of_board / 30) / 2
# symbol_thickness = 3
# symbol_X_color = '#EE4035'
# symbol_O_color = '#0492CF'
# Green_color = '#7BC043'

# game_instance = Tic_Tac_Toe()
# game_instance.mainloop()