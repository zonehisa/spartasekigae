from typing import List, Dict
from collections import defaultdict
import random
from .config import Config


class SeatingManager:
    def __init__(self):
        self.participants: List[str] = Config.DEFAULT_PARTICIPANTS.copy()
        self.current_seating: Dict[str, List[str]] = {
            "seats": [self.participants[i] if i is not None else "" for i in Config.SEAT_LAYOUT]
        }

    def get_table_number(self, index: int) -> int:
        """座席インデックスからテーブル番号（0-4）を取得"""
        return index // 5

    def get_table_members(self, seats: List[str]) -> Dict[int, List[str]]:
        """各テーブルのメンバーを取得"""
        table_members = defaultdict(list)
        for i, seat in enumerate(seats):
            if seat:
                table_members[self.get_table_number(i)].append(seat)
        return table_members

    def is_valid_seating(self, previous_seats: List[str], new_seats: List[str]) -> bool:
        """配置の妥当性チェック"""
        # 同じ席チェック
        if any(prev == new and prev for prev, new in zip(previous_seats, new_seats)):
            return False

        # テーブルメンバーの重複チェック
        prev_tables = self.get_table_members(previous_seats)
        new_tables = self.get_table_members(new_seats)

        for new_table_num, new_members in new_tables.items():
            for prev_table_num, prev_members in prev_tables.items():
                common_members = set(new_members) & set(prev_members)
                if len(common_members) >= 3:
                    return False
        return True

    def shuffle_seats(self) -> Dict[str, List[str]]:
        """席をシャッフル"""
        previous_seating = self.current_seating["seats"].copy()

        for attempt in range(Config.MAX_SHUFFLE_ATTEMPTS):
            shuffled_participants = self.participants.copy()
            random.shuffle(shuffled_participants)

            new_seats = []
            participant_index = 0

            for seat in Config.SEAT_LAYOUT:
                if seat is None:
                    new_seats.append("")
                else:
                    new_seats.append(shuffled_participants[participant_index])
                    participant_index += 1

            if self.is_valid_seating(previous_seating, new_seats):
                self.current_seating["seats"] = new_seats
                return self.current_seating

        raise ValueError("有効な席配置が見つかりませんでした。")

    def update_participants(self, new_participants: List[str]) -> None:
        """参加者リストの更新"""
        if not Config.MIN_PARTICIPANTS <= len(new_participants) <= Config.MAX_PARTICIPANTS:
            raise ValueError(
                f"参加者は{Config.MIN_PARTICIPANTS}名以上{Config.MAX_PARTICIPANTS}名以下である必要があります"
            )

        if len(set(new_participants)) != len(new_participants):
            raise ValueError("参加者名が重複しています")

        if any(not name.strip() for name in new_participants):
            raise ValueError("空の参加者名は使用できません")

        self.participants = new_participants
        self.current_seating = {
            "seats": [self.participants[i] if i is not None else "" for i in Config.SEAT_LAYOUT]
        }
