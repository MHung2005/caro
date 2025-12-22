"""
Game utilities for Caro: winner detection and tie checks.
These helpers centralize the core game rules separate from UI.
"""
from typing import Iterable
import numpy as np


WIN_LENGTH = 5


def check_winner(board: np.ndarray, player: int, win_len: int = WIN_LENGTH) -> bool:
    """
    Return True if `player` has a contiguous sequence of `win_len` on the board.
    `board` is expected to be a 2D numpy array with values in {1, -1, 0}.
    """
    b = np.asarray(board)
    n = b.shape[0]

    # Rows
    for r in range(n):
        for c in range(n - win_len + 1):
            if np.all(b[r, c : c + win_len] == player):
                return True

    # Columns
    for c in range(n):
        for r in range(n - win_len + 1):
            if np.all(b[r : r + win_len, c] == player):
                return True

    # Diagonals (\)
    for r in range(n - win_len + 1):
        for c in range(n - win_len + 1):
            if all(b[r + i, c + i] == player for i in range(win_len)):
                return True

    # Anti-diagonals (/)
    for r in range(n - win_len + 1):
        for c in range(win_len - 1, n):
            if all(b[r + i, c - i] == player for i in range(win_len)):
                return True

    return False


def is_tie(board: np.ndarray) -> bool:
    """Return True if the board has no empty (0) cells."""
    b = np.asarray(board)
    return not (b == 0).any()


def is_cell_empty(board: np.ndarray, r: int, c: int) -> bool:
    """Return True if cell (r, c) is empty on the board."""
    return board[r][c] == 0
