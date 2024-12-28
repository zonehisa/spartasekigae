from typing import List


class Config:
    DEFAULT_PARTICIPANTS = [f"参加者{i+1}" for i in range(15)]
    MAX_PARTICIPANTS = 15
    MIN_PARTICIPANTS = 1
    MAX_HISTORY_SIZE = 10
    MAX_SHUFFLE_ATTEMPTS = 200
    SEAT_LAYOUT = [
        0,
        4,
        None,
        5,
        9,
        1,
        3,
        None,
        6,
        8,
        2,
        None,
        None,
        None,
        7,
        None,
        None,
        None,
        None,
        None,
        10,
        11,
        12,
        13,
        14,
    ]
