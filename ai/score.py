import numpy as np

# Trọng số đánh giá (có thể điều chỉnh)
SCORES = {
    5: 1_000_000,
    4: 100_000,   # both-open
    (4, 'half'): 10_000,  # one side blocked
    3: 1_000,     # both-open
    (3, 'half'): 100,
    2: 50,        # both-open
    (2, 'half'): 10,
    1: 5,
    (1, 'half'): 2
}


def _score_line(arr, player):
    """
    Đánh giá một mảng 1D (hàng, cột hoặc đường chéo).
    Trả về tổng điểm của player trên line này.
    """
    n = len(arr)
    s = 0
    i = 0
    while i < n:
        if arr[i] != player:
            i += 1
            continue
        # tìm độ dài chuỗi liên tiếp của player bắt đầu từ i
        j = i
        while j < n and arr[j] == player:
            j += 1
        length = j - i
        left = i - 1
        right = j
        left_open = left >= 0 and arr[left] == 0
        right_open = right < n and arr[right] == 0

        if length >= 5:
            return SCORES[5]  # thắng tuyệt đối, trả ngay giá trị lớn
        if length == 4:
            if left_open and right_open:
                s += SCORES[4]
            elif left_open or right_open:
                s += SCORES[(4, 'half')]
        elif length == 3:
            if left_open and right_open:
                s += SCORES[3]
            elif left_open or right_open:
                s += SCORES[(3, 'half')]
        elif length == 2:
            if left_open and right_open:
                s += SCORES[2]
            elif left_open or right_open:
                s += SCORES[(2, 'half')]
        elif length == 1:
            if left_open and right_open:
                s += SCORES[1]
            elif left_open or right_open:
                s += SCORES[(1, 'half')]

        i = j  # nhảy sang sau đoạn đã tính
    return s


def evaluate_board(board, player):
    """
    Đánh giá toàn bộ bàn cờ cho `player` (1 hoặc -1).
    Trả về score = score(player) - score(opponent).
    board: numpy array shape (15,15) với values {1, -1, 0}
    """
    b = np.asarray(board, dtype=int)
    n = b.shape[0]
    player_score = 0
    opp = -player
    opp_score = 0

    # Hàng
    for r in range(n):
        row = b[r, :]
        player_score += _score_line(row, player)
        opp_score += _score_line(row, opp)

    # Cột
    for c in range(n):
        col = b[:, c]
        player_score += _score_line(col, player)
        opp_score += _score_line(col, opp)

    # Chéo chính (r - c = const)
    for d in range(-n + 1, n):
        diag = b.diagonal(offset=d)
        if diag.size >= 1:
            player_score += _score_line(diag, player)
            opp_score += _score_line(diag, opp)

    # Chéo phụ (flip trái-phải rồi lấy diagonal)
    bf = np.fliplr(b)
    for d in range(-n + 1, n):
        diag = bf.diagonal(offset=d)
        if diag.size >= 1:
            player_score += _score_line(diag, player)
            opp_score += _score_line(diag, opp)

    # Trả về hiệu (có thể cân bằng trọng số nếu muốn)
    return int(player_score - opp_score)