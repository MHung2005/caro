import random
from typing import Tuple, Optional


class AIEasy:
    """Very simple AI: picks a random empty cell.

    Maintains a node_count interface compatible with other AIs
    for logging purposes.
    """

    def __init__(self, symbol: int):
        self.symbol = symbol
        self.node_count = 0

    def choose_move(self, board_status) -> Tuple[Optional[tuple], int]:
        # Chuẩn hoá: node_count = số ô trống đã duyệt (scan) như chi phí quyết định
        size = len(board_status)
        empty_cells = [
            (r, c)
            for r in range(size)
            for c in range(size)
            if board_status[r][c] == 0
        ]
        self.node_count = len(empty_cells)
        move = random.choice(empty_cells) if empty_cells else None
        return move, self.node_count
