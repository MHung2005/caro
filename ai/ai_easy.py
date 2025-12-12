import random

class AIEasy:
    def __init__(self, symbol):
        self.symbol = symbol
        self.node_count = 0
    def choose_move(self, board_status, num_board = 10):
        empty_cells = [
            (r, c) for r in range(num_board)
            for c in range(num_board)
            if board_status[r][c] == 0
        ]
        return random.choice(empty_cells), self.node_count
