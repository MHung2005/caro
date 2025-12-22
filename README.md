# Caro (Gomoku) – Tkinter

A simple 10x10 Caro/Gomoku game with Human (X) vs AI (O) using Tkinter.

## Structure
- `main.py`: Tkinter UI and app orchestration
- `config.py`: Centralized constants for board/UI
- `game.py`: Game utilities (winner/tie checks)
- `ai/`: AI implementations and scoring
  - `ai_easy.py`: Random-move baseline AI
  - `ai_minimax.py`: Minimax AI
  - `ai_hard.py`: Minimax + Alpha-Beta pruning
  - `score.py`: Heuristic evaluator

## Run
```bash
python main.py
```

## Notes
- The UI constants (board size, colors) are centralized in `config.py`.
- Winner/tie detection is centralized in `game.py` and used by the UI.
- All AIs implement `choose_move(board) -> (move, node_count)` for consistent logging.

### Node Count Semantics
- Minimax / Alpha-Beta: `node_count` ~= số node duyệt trong cây tìm kiếm (mỗi lần gọi hàm đệ quy được tính là 1 node).
- Easy (random): `node_count` = số ô trống được quét (scan) trước khi chọn ngẫu nhiên, xem như chi phí quyết định ở mức cơ bản.