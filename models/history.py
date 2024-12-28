from typing import List, Dict
import json
from datetime import datetime
from .config import Config


class HistoryManager:
    @staticmethod
    def load_history() -> List[Dict]:
        """座席履歴の読み込み"""
        try:
            with open("seating_history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_history(history: List[Dict]) -> None:
        """座席履歴の保存"""
        with open("seating_history.json", "w", encoding="utf-8") as f:
            json.dump(history, indent=2, ensure_ascii=False, fp=f)

    @staticmethod
    def add_to_history(seating: Dict[str, List[str]]) -> None:
        """新しい配置を履歴に追加"""
        history = HistoryManager.load_history()
        new_arrangement = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "seats": seating["seats"]}
        history.insert(0, new_arrangement)
        history = history[: Config.MAX_HISTORY_SIZE]
        HistoryManager.save_history(history)
