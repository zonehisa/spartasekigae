from typing import List, Dict


class Config:
    DEFAULT_PARTICIPANTS = [f"参加者{i+1}" for i in range(15)]
    MAX_PARTICIPANTS = 15
    MIN_PARTICIPANTS = 1
    MAX_HISTORY_SIZE = 10
    MAX_SHUFFLE_ATTEMPTS = 200

    # 基本の席レイアウト（Noneは空席を表す）
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

    # 参加者数に応じて無効化する席番号（インデックスではなく、実際の席番号）
    SEATS_TO_REMOVE: Dict[int, List[int]] = {
        14: [14],  # 14名の場合、14番の席を無効化
        13: [14, 10],  # 13名の場合、14番と10番の席を無効化
        12: [14, 10, 13],
        11: [14, 10, 13, 11],
        10: [14, 10, 13, 11, 12],
    }

    @classmethod
    def get_valid_seat_numbers(cls, participant_count: int) -> List[int]:
        """参加者数に応じた有効な席番号のリストを返す"""
        if participant_count >= cls.MAX_PARTICIPANTS:
            return list(range(cls.MAX_PARTICIPANTS))

        seats_to_remove = cls.SEATS_TO_REMOVE.get(participant_count, [])
        return [i for i in range(cls.MAX_PARTICIPANTS) if i not in seats_to_remove]
