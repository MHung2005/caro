import math
import numpy as np

from ai.score import evaluate_board

AI = 1        # O (máy)
PLAYER = -1   # X (người)
EMPTY = 0
SIZE = 10


class AIHard:
    def __init__(self, ai_player=AI, max_depth=2):
        """
        ai_player: 1 hoặc -1 (trong project của bạn: O = 1, X = -1)
        max_depth: độ sâu minimax (2, 3, ...)
        """
        self.ai = ai_player
        self.human = -ai_player
        self.max_depth = max_depth

    # ---------------- is_full (METHOD) ----------------
    def is_full(self, board):
        """Trả về True nếu bàn cờ không còn ô trống."""
        b = np.asarray(board)
        return not (b == EMPTY).any()

    # ---------------- check_win (METHOD) ----------------
    def check_win(self, board, player):
        """
        Kiểm tra player (1 hoặc -1) đã thắng chưa (5 quân liên tiếp).
        board là numpy array 10x10.
        """
        n = SIZE
        win_len = 5
        b = np.asarray(board)

        # hàng ngang
        for r in range(n):
            for c in range(n - win_len + 1):
                if np.all(b[r, c:c+win_len] == player):
                    return True

        # cột dọc
        for c in range(n):
            for r in range(n - win_len + 1):
                if np.all(b[r:r+win_len, c] == player):
                    return True

        # chéo chính ↘
        for r in range(n - win_len + 1):
            for c in range(n - win_len + 1):
                if all(b[r+i, c+i] == player for i in range(win_len)):
                    return True

        # chéo phụ ↙
        for r in range(n - win_len + 1):
            for c in range(win_len - 1, n):
                if all(b[r+i, c-i] == player for i in range(win_len)):
                    return True

        return False

    # ---------------- has_neighbor (METHOD) ----------------
    def has_neighbor(self, board, r, c, dist=2):
        """
        Kiểm tra xem ô (r, c) có ít nhất một quân cờ nào
        trong phạm vi 'dist' ô xung quanh hay không.
        """
        n = SIZE
        b = np.asarray(board)
        for dr in range(-dist, dist + 1):
            for dc in range(-dist, dist + 1):
                if dr == 0 and dc == 0:
                    continue  # bỏ qua chính ô (r, c)

                rr = r + dr
                cc = c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    if b[rr][cc] != EMPTY:
                        return True
        return False

    # ---------------- generate_moves (METHOD) ----------------
    def generate_moves(self, board):
        """
        Sinh danh sách các nước đi khả thi cho AI:
        - Chỉ lấy những ô TRỐNG (== EMPTY)
        - Và xung quanh nó (bán kính dist) có ít nhất một quân cờ.
        Nếu bàn còn trống hoàn toàn → trả về ô chính giữa.
        """
        n = SIZE
        b = np.asarray(board)
        moves = []

        for r in range(n):
            for c in range(n):
                if b[r][c] == EMPTY and self.has_neighbor(b, r, c, dist=2):
                    moves.append((r, c))

        # Nếu bàn hoàn toàn trống
        if not moves:
            moves.append((n // 2, n // 2))  # (5,5) trên bàn 10x10

        return moves

    # ---------------- minimax (METHOD) ----------------
    def minimax(self, board, depth, alpha, beta, maximizing, current_player):
        """
        Minimax + alpha-beta trên board (numpy 10x10).
        current_player: self.ai (1) hoặc self.human (-1).
        maximizing: True nếu node MAX (AI), False nếu node MIN (người).
        """
        b = np.asarray(board)

        # 1. Trường hợp cơ sở: có người thắng / hết sâu / đầy bàn
        if self.check_win(b, self.ai):
            return 10**9
        if self.check_win(b, self.human):
            return -10**9
        if depth == 0 or self.is_full(b):
            # Đánh giá từ góc nhìn AI
            return evaluate_board(b, self.ai)

        moves = self.generate_moves(b)
        if not moves:
            return 0

        # 2. Node MAX (AI)
        if maximizing:
            value = -math.inf
            for (x, y) in moves:
                b[x][y] = current_player
                next_player = self.human if current_player == self.ai else self.ai

                score = self.minimax(
                    b,
                    depth - 1,
                    alpha,
                    beta,
                    False,        # sau MAX là MIN
                    next_player
                )
                b[x][y] = EMPTY

                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:     # cắt tỉa BETA
                    break
            return value

        # 3. Node MIN (người)
        else:
            value = math.inf
            for (x, y) in moves:
                b[x][y] = current_player
                next_player = self.human if current_player == self.ai else self.ai

                score = self.minimax(
                    b,
                    depth - 1,
                    alpha,
                    beta,
                    True,         # sau MIN là MAX
                    next_player
                )
                b[x][y] = EMPTY

                value = min(value, score)
                beta = min(beta, value)
                if beta <= alpha:     # cắt tỉa ALPHA
                    break
            return value

    # ---------------- find_best_move (METHOD) ----------------
    def find_best_move(self, board):
        """
        Tìm nước đi tốt nhất cho AI (self.ai) trên 'board'.
        board: numpy array 10x10.
        Trả về (r, c) hoặc None nếu không có nước đi.
        """
        b = np.array(board, copy=True)
        best_value = -math.inf
        best_move = None

        moves = self.generate_moves(b)
        if not moves:
            return None

        for (x, y) in moves:
            b[x][y] = self.ai
            score = self.minimax(
                b,
                self.max_depth - 1,
                -math.inf,
                math.inf,
                False,   # sau khi AI đi, đến lượt MIN (người)
                self.human
            )
            b[x][y] = EMPTY

            if score > best_value:
                best_value = score
                best_move = (x, y)

        return best_move

    # ---------------- choose_move (METHOD) ----------------
    def choose_move(self, board_status):
        board_copy = np.array(board_status, copy=True)
        return self.find_best_move(board_copy)