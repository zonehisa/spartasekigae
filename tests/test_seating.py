import unittest
from models.seating import SeatingManager
from models.config import Config


class TestSeatingManager(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行される"""
        self.manager = SeatingManager()
        self.test_participants = ["Alice", "Bob", "Charlie", "David", "Eve"]

    def test_create_seating_layout(self):
        """座席レイアウト作成のテスト"""
        self.manager.participants = self.test_participants
        layout = self.manager.create_seating_layout()

        # レイアウトの長さが正しいか
        self.assertEqual(len(layout), len(Config.SEAT_LAYOUT))

        # 参加者が全て配置されているか
        placed_participants = [seat for seat in layout if seat]
        self.assertEqual(len(placed_participants), len(self.test_participants))

        # 全ての参加者が含まれているか
        for participant in self.test_participants:
            self.assertIn(participant, layout)

    def test_shuffle_seats(self):
        """席替えのテスト"""
        self.manager.participants = self.test_participants
        original_seating = self.manager.current_seating["seats"].copy()

        # 席替えを実行
        new_seating = self.manager.shuffle_seats()

        # 新しい配置が返されているか
        self.assertIsNotNone(new_seating)
        self.assertIn("seats", new_seating)

        # 全ての参加者が含まれているか
        new_seats = new_seating["seats"]
        for participant in self.test_participants:
            self.assertIn(participant, new_seats)

        # 配置が変更されているか
        self.assertNotEqual(original_seating, new_seats)

    def test_move_seat(self):
        """席の移動テスト"""
        self.manager.participants = self.test_participants
        self.manager.current_seating = {
            "seats": ["Alice", "Bob", "", "Charlie", "David", "", "Eve", "", "", ""]
        }

        # 通常の移動テスト
        new_seating = self.manager.move_seat(0, 2, False)
        self.assertEqual(new_seating["seats"][2], "Alice")
        self.assertEqual(new_seating["seats"][0], "")

        # 席の交換テスト
        new_seating = self.manager.move_seat(1, 3, True)
        self.assertEqual(new_seating["seats"][1], "Charlie")
        self.assertEqual(new_seating["seats"][3], "Bob")

    def test_invalid_moves(self):
        """無効な移動のテスト"""
        self.manager.participants = self.test_participants
        self.manager.current_seating = {
            "seats": ["Alice", "Bob", "", "Charlie", "David", "", "Eve", "", "", ""]
        }

        # 範囲外の移動
        with self.assertRaises(ValueError):
            self.manager.move_seat(-1, 0, False)

        # 空席からの移動
        with self.assertRaises(ValueError):
            self.manager.move_seat(2, 0, False)

        # 使用中の席への移動（交換モードでない場合）
        with self.assertRaises(ValueError):
            self.manager.move_seat(0, 1, False)

    def test_update_participants(self):
        """参加者リスト更新のテスト"""
        new_participants = ["Alice", "Bob", "Charlie"]
        self.manager.update_participants(new_participants)

        # 参加者リストが更新されているか
        self.assertEqual(self.manager.participants, new_participants)

        # 座席が更新されているか
        seats = self.manager.current_seating["seats"]
        for participant in new_participants:
            self.assertIn(participant, seats)

    def test_invalid_participants(self):
        """無効な参加者リストのテスト"""
        # 重複した参加者
        with self.assertRaises(ValueError):
            self.manager.update_participants(["Alice", "Alice", "Bob"])

        # 空の参加者名
        with self.assertRaises(ValueError):
            self.manager.update_participants(["Alice", "", "Bob"])

        # 参加者数が多すぎる
        too_many = ["P" + str(i) for i in range(Config.MAX_PARTICIPANTS + 1)]
        with self.assertRaises(ValueError):
            self.manager.update_participants(too_many)


if __name__ == "__main__":
    unittest.main()
