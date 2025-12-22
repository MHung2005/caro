"""
Central configuration for Caro (Gomoku) app.

Holds UI sizes, colors, and grid configuration to keep values
consistent across modules.
"""

# Board/grid configuration
GRID_SIZE: int = 10  # 10x10 board
BOARD_SIZE_PX: int = 600  # canvas size in pixels

# Symbol rendering
SYMBOL_THICKNESS: int = 3

# Derived symbol size (kept consistent with original formula)
SYMBOL_SIZE: float = (BOARD_SIZE_PX / 10 - BOARD_SIZE_PX / 30) / 2

# Colors
COLOR_X: str = "#EE4035"
COLOR_O: str = "#0492CF"
COLOR_GREEN: str = "#7BC043"
