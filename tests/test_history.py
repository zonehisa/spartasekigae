import unittest
import os
from models.history import HistoryManager


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        """各テストの前に実行される"""
        # テスト用の履歴データ
        self.test_history = [
            {"date": "2024-01-01 10:00:00", "seats": ["A", "B", "C", "", "", "D", "E", "F", "", ""]}
        ]
        # オリジナルのファイル名を保存
        self.original_file = "seating_history.json"
        self.original_exists = os.path.exists(self.original_file)
        if self.original_exists:
            self.original_backup = self.original_file + ".backup"
            os.rename(self.original_file, self.original_backup)

    def tearDown(self):
        """各テストの後に実行される"""
        # テストファイルを削除
        if os.path.exists(self.original_file):
            os.remove(self.original_file)
        # オリジナルファイルを復元
        if self.original_exists:
            os.rename(self.original_backup, self.original_file)

    def test_save_and_load_history(self):
        """履歴の保存と読み込みのテスト"""
        # 履歴を保存
        HistoryManager.save_history(self.test_history)

        # 履歴を���み込み
        loaded_history = HistoryManager.load_history()

        # 読み込んだデータが正しいか確認
        self.assertEqual(len(loaded_history), 1)
        self.assertEqual(loaded_history[0]["seats"], self.test_history[0]["seats"])

    def test_clear_history(self):
        """履歴クリアのテスト"""
        # まず履歴を保存
        HistoryManager.save_history(self.test_history)

        # 履歴をクリア
        HistoryManager.save_history([])

        # 履歴が空になっているか確認
        loaded_history = HistoryManager.load_history()
        self.assertEqual(len(loaded_history), 0)

    def test_add_to_history(self):
        """履歴追加のテスト"""
        # 新しい配置を追加
        new_seating = {"seats": ["X", "Y", "Z", "", "", "P", "Q", "R", "", ""]}
        HistoryManager.add_to_history(new_seating)

        # 履歴を読み込んで確認
        loaded_history = HistoryManager.load_history()
        self.assertEqual(len(loaded_history), 1)
        self.assertEqual(loaded_history[0]["seats"], new_seating["seats"])


if __name__ == "__main__":
    unittest.main()
