import math
import numpy as np
from ai.score import evaluate_board

AI = 1
PLAYER = -1
EMPTY = 0
SIZE = 10

class AIMinimax:
    def __init__(self, ai_player=AI, max_depth=2):
        self.ai = ai_player
        self.human = -ai_player
        self.max_depth = max_depth
    #----------count node----------
        self.node_count = 0
    def reset_counter(self):
        self.node_count = 0
    # ----------- is_full -----------
    def is_full(self, board):
        return not (np.asarray(board) == EMPTY).any()

    # ----------- check_win -----------
    def check_win(self, board, player):
        n = SIZE
        win_len = 5
        b = np.asarray(board)

        # hàng ngang
        for r in range(n):
            for c in range(n - win_len + 1):
                if np.all(b[r, c:c + win_len] == player):
                    return True

        # cột
        for c in range(n):
            for r in range(n - win_len + 1):
                if np.all(b[r:r + win_len, c] == player):
                    return True

        # chéo chính
        for r in range(n - win_len + 1):
            for c in range(n - win_len + 1):
                if all(b[r + i, c + i] == player for i in range(win_len)):
                    return True

        # chéo phụ
        for r in range(n - win_len + 1):
            for c in range(win_len - 1, n):
                if all(b[r + i, c - i] == player for i in range(win_len)):
                    return True

        return False

    # ----------- has_neighbor -----------
    def has_neighbor(self, board, r, c, dist=2):
        b = np.asarray(board)
        for dr in range(-dist, dist + 1):
            for dc in range(-dist, dist + 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < SIZE and 0 <= cc < SIZE:
                    if board[rr][cc] != EMPTY:
                        return True
        return False

    # ----------- generate_moves -----------
    def generate_moves(self, board):
        moves = []
        for r in range(SIZE):
            for c in range(SIZE):
                if board[r][c] == EMPTY and self.has_neighbor(board, r, c, dist=2):
                    moves.append((r, c))

        if not moves:
            moves.append((SIZE // 2, SIZE // 2))
        return moves

    # ----- MAX-VALUE(state) -----
    def max_value(self, board, depth):
        self.node_count += 1

        if self.check_win(board, self.ai):
            return 10**9
        if self.check_win(board, self.human):
            return -10**9
        if depth == 0 or self.is_full(board):
            return evaluate_board(board, self.ai)

        v = -math.inf
        moves = self.generate_moves(board)

        for (x, y) in moves:
            board[x][y] = self.ai
            v = max(v, self.min_value(board, depth - 1))
            board[x][y] = EMPTY

        return v

    # ----- MIN-VALUE(state) -----
    def min_value(self, board, depth):
        self.node_count += 1

        if self.check_win(board, self.ai):
            return 10**9
        if self.check_win(board, self.human):
            return -10**9
        if depth == 0 or self.is_full(board):
            return evaluate_board(board, self.ai)

        v = math.inf
        moves = self.generate_moves(board)

        for (x, y) in moves:
            board[x][y] = self.human
            v = min(v, self.max_value(board, depth - 1))
            board[x][y] = EMPTY

        return v
        
    # ----- Minimax-Decision -----
    def minimax_decision(self, board):

        moves = self.generate_moves(board)
        best_value = -math.inf
        best_move = None

        for (x, y) in moves:
            board[x][y] = self.ai
            v = self.min_value(board, self.max_depth - 1)
            board[x][y] = EMPTY

            if v > best_value:
                best_value = v
                best_move = (x, y)

        return best_move

    def choose_move(self, board):
        self.reset_counter()
        board_copy = np.array(board, copy=True)
        return self.minimax_decision(board_copy)