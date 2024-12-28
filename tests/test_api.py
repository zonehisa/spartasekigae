import unittest
import json
from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行される"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """インデックスページのテスト"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_shuffle(self):
        """席替えAPIのテスト"""
        response = self.app.get("/shuffle")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("seats", data)

    def test_update_participants(self):
        """参加者更新APIのテスト"""
        test_data = {"participants": ["Alice", "Bob", "Charlie"]}
        response = self.app.post("/update_participants", json=test_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("message", data)

    def test_invalid_update_participants(self):
        """無効な参加者更新のテスト"""
        # 重複した参加者
        test_data = {"participants": ["Alice", "Alice", "Bob"]}
        response = self.app.post("/update_participants", json=test_data)
        self.assertEqual(response.status_code, 400)

    def test_move_seat(self):
        """席移動APIのテスト"""
        # まず参加者を設定
        self.app.post("/update_participants", json={"participants": ["Alice", "Bob", "Charlie"]})

        # 席の移動をテスト
        test_data = {"from_pos": 0, "to_pos": 2, "is_swap": False}
        response = self.app.post("/move_seat", json=test_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("seats", data)

    def test_invalid_move_seat(self):
        """無効な席移動のテスト"""
        test_data = {"from_pos": -1, "to_pos": 0, "is_swap": False}  # 無効な位置
        response = self.app.post("/move_seat", json=test_data)
        self.assertEqual(response.status_code, 400)

    def test_clear_history(self):
        """履歴クリアのテスト"""
        response = self.app.post("/clear_history")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("message", data)


if __name__ == "__main__":
    unittest.main()
