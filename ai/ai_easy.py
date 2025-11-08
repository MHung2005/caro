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
