from typing import List, Dict
from collections import defaultdict
import random
from .config import Config


class SeatingManager:
    def __init__(self):
        self.participants: List[str] = Config.DEFAULT_PARTICIPANTS.copy()
        self.current_seating: Dict[str, List[str]] = {"seats": self.create_seating_layout()}

    def create_seating_layout(self, maintain_order: bool = True) -> List[str]:
        """
        参加者数に応じた席レイアウトを作成
        Args:
            maintain_order: Trueの場合、参加者リストの順番を席の順番に反映
        """
        layout = Config.SEAT_LAYOUT.copy()
        participant_count = len(self.participants)
        valid_seat_numbers = Config.get_valid_seat_numbers(participant_count)

        # 有効な席のインデックスを取得（Noneでない席のうち、有効な席番号に対応するもの）
        valid_indices = [
            i for i, seat in enumerate(layout) if seat is not None and seat in valid_seat_numbers
        ]

        # 順番を維持する場合は、席番号の順にソート
        if maintain_order:
            valid_indices.sort(key=lambda i: layout[i])

        # 新しい席配置を作成
        result = [""] * len(layout)
        for idx, seat_idx in enumerate(valid_indices):
            if idx < len(self.participants):  # 参加者数分だけ割り当て
                result[seat_idx] = self.participants[idx]

        return result

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
        layout = Config.SEAT_LAYOUT.copy()
        valid_seat_numbers = Config.get_valid_seat_numbers(len(self.participants))

        for attempt in range(Config.MAX_SHUFFLE_ATTEMPTS):
            shuffled_participants = self.participants.copy()
            random.shuffle(shuffled_participants)

            # 有効な席のインデックスを取得
            valid_indices = [
                i for i, seat in enumerate(layout) if seat is not None and seat in valid_seat_numbers
            ]

            # シャッフル時は席番号でソートしない（ランダムな配置を維持）
            new_seats = [""] * len(layout)
            for idx, participant_idx in enumerate(valid_indices):
                if idx < len(shuffled_participants):  # 参加者数分だけ割り当て
                    new_seats[participant_idx] = shuffled_participants[idx]

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

        self.participants = new_participants.copy()  # 参加者リストをコピーして保存
        # 参加者リストの更新時は順番を維持
        self.current_seating = {"seats": self.create_seating_layout(maintain_order=True)}

    def move_seat(self, from_pos: int, to_pos: int, is_swap: bool = False) -> Dict[str, List[str]]:
        """
        席の移動または交換を行う
        Args:
            from_pos: 移動元の席のインデックス
            to_pos: 移動先の席のインデックス
            is_swap: Trueの場合は席の交換、Falseの場合は移動
        """
        if (
            from_pos < 0
            or from_pos >= len(self.current_seating["seats"])
            or to_pos < 0
            or to_pos >= len(self.current_seating["seats"])
        ):
            raise ValueError("無効な席番号です")

        # 移動元の席が空の場合はエラー
        if not self.current_seating["seats"][from_pos]:
            raise ValueError("移動元の席が空です")

        # 移動先の席が空でない場合は交換モードが必要
        if self.current_seating["seats"][to_pos] and not is_swap:
            raise ValueError("移動先の席が既に使用されています")

        # 席の配置をコピー
        new_seats = self.current_seating["seats"].copy()

        # 席の交換または移動
        if is_swap:
            new_seats[from_pos], new_seats[to_pos] = new_seats[to_pos], new_seats[from_pos]
        else:
            new_seats[to_pos] = new_seats[from_pos]
            new_seats[from_pos] = ""

        # 新しい配置を保存
        self.current_seating["seats"] = new_seats
        return self.current_seating
