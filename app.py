from flask import Flask, render_template, jsonify, request
import random
from collections import defaultdict
import json
from datetime import datetime

app = Flask(__name__)

# デフォルトの参加者リスト
DEFAULT_PARTICIPANTS = [f"参加者{i+1}" for i in range(15)]

# 現在の参加者リスト
participants = DEFAULT_PARTICIPANTS.copy()

# 5×5のグリッドでの席の配置（Noneは空席を表す）
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

# 参加者数に応じてシートレイアウトを調整
if len(participants) == 14:
    SEAT_LAYOUT[10] = None  # 10番目の席を空席に
elif len(participants) == 13:
    SEAT_LAYOUT[14] = None  # 14番目の席を空席に
elif len(participants) == 12:
    SEAT_LAYOUT[11] = None  # 11番目の席を空席に
elif len(participants) == 11:
    SEAT_LAYOUT[12] = None  # 12番目の席を空席に

# 現在の席配置を保存
current_seating = {"seats": [participants[i] if i is not None else "" for i in SEAT_LAYOUT]}


def get_table_number(index):
    """座席インデックスからテーブル番号（0-4）を取得"""
    return index // 5


def get_table_members(seats):
    """各テーブルのメンバーを取得"""
    table_members = defaultdict(list)
    for i, seat in enumerate(seats):
        if seat:  # 空席でない場合
            table_members[get_table_number(i)].append(seat)
    return table_members


def is_valid_seating(previous_seats, new_seats):
    """
    前回の配置と新しい配置をチェック
    1. 同じテーブルに3人以上のメンバーが重複していないか
    2. 同じ席に同じ人が座っていないか
    """
    # 同じ席チェック
    for i, (prev_seat, new_seat) in enumerate(zip(previous_seats, new_seats)):
        if prev_seat and new_seat and prev_seat == new_seat:
            return False

    # テーブルメンバーの重複チェック
    prev_tables = get_table_members(previous_seats)
    new_tables = get_table_members(new_seats)

    # 各テーブルについて、前回のメンバーとの重複をチェック
    for new_table_num, new_members in new_tables.items():
        for prev_table_num, prev_members in prev_tables.items():
            # 同じメンバーが3人以上重複している場合は無効
            common_members = set(new_members) & set(prev_members)
            if len(common_members) >= 3:
                return False
    return True


# 座席履歴をJSONファイルから読み込む
def load_seating_history():
    try:
        with open("seating_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# 座席履歴をJSONファイルに保存
def save_seating_history(history):
    with open("seating_history.json", "w", encoding="utf-8") as f:
        json.dump(history, indent=2, ensure_ascii=False, fp=f)


@app.route("/")
def index():
    history = load_seating_history()
    return render_template("index.html", seating=current_seating, participants=participants, history=history)


@app.route("/get_history")
def get_history():
    history = load_seating_history()
    return jsonify(history)


@app.route("/update_participants", methods=["POST"])
def update_participants():
    global participants, current_seating
    try:
        new_participants = request.json.get("participants", [])
        if len(new_participants) < 1:
            return jsonify({"error": "参加者は1名以上である必要があります"}), 400
        if len(new_participants) > 15:
            return jsonify({"error": "参加者は15名以下である必要があります"}), 400

        # 重複チェック
        if len(set(new_participants)) != len(new_participants):
            return jsonify({"error": "参加者名が重複しています"}), 400

        # 空文字チェック
        if any(not name.strip() for name in new_participants):
            return jsonify({"error": "空の参加者名は使用できません"}), 400

        participants = new_participants
        current_seating = {"seats": [participants[i] if i is not None else "" for i in SEAT_LAYOUT]}
        return jsonify({"message": "参加者リストを更新しました"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/shuffle")
def shuffle_seats():
    global current_seating

    # 前回の配置を保存
    previous_seating = current_seating["seats"].copy()

    max_attempts = 200
    attempt = 0

    while attempt < max_attempts:
        # 参加者リストをシャッフル
        shuffled_participants = participants.copy()
        random.shuffle(shuffled_participants)

        # 新しい配置を作成（空席の位置は保持）
        new_seats = []
        participant_index = 0

        for seat in SEAT_LAYOUT:
            if seat is None:
                new_seats.append("")
            else:
                new_seats.append(shuffled_participants[participant_index])
                participant_index += 1

        # 前回のテーブルメンバーと重複していないかチェック
        if is_valid_seating(previous_seating, new_seats):
            current_seating["seats"] = new_seats
            break

        attempt += 1

    if attempt >= max_attempts:
        return (
            jsonify(
                {"error": "有効な席配置が見つかりませんでした。\n前回と異なる配置を生成できませんでした。"}
            ),
            400,
        )

    # 履歴に新しい配置を追加
    history = load_seating_history()
    new_arrangement = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seats": current_seating["seats"],
    }
    history.insert(0, new_arrangement)  # 新しい配置を先頭に追加

    # 最新の10件のみを保持
    history = history[:10]
    save_seating_history(history)

    return jsonify(current_seating)


@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        # 空の履歴リストで���書き保存
        save_seating_history([])
        return jsonify({"message": "履歴をクリアしました"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
