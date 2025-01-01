from flask import Flask, render_template, jsonify, request
from models.seating import SeatingManager
from models.history import HistoryManager


# Flaskアプリケーションの初期化
app = Flask(__name__)
seating_manager = SeatingManager()


@app.route("/")
def index():
    history = HistoryManager.load_history()
    return render_template(
        "index.html",
        seating=seating_manager.current_seating,
        participants=seating_manager.participants,
        history=history,
    )


@app.route("/get_history")
def get_history():
    return jsonify(HistoryManager.load_history())


@app.route("/update_participants", methods=["POST"])
def update_participants():
    try:
        new_participants = request.json.get("participants", [])
        seating_manager.update_participants(new_participants)
        return jsonify({"message": "参加者リストを更新しました"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "予期せぬエラーが発生しました"}), 500


@app.route("/shuffle")
def shuffle_seats():
    try:
        # 現在の配置を履歴として保存
        HistoryManager.add_to_history(seating_manager.current_seating)
        # 新しい配置を生成
        new_seating = seating_manager.shuffle_seats()
        return jsonify(new_seating)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "予期せぬエラーが発生しました"}), 500


@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        HistoryManager.save_history([])
        return jsonify({"message": "履歴をクリアしました"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/move_seat", methods=["POST"])
def move_seat():
    try:
        from_pos = request.json.get("from_pos")
        to_pos = request.json.get("to_pos")
        is_swap = request.json.get("is_swap", False)

        new_seating = seating_manager.move_seat(from_pos, to_pos, is_swap)
        return jsonify(new_seating)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "予期せぬエラーが発生しました"}), 500


if __name__ == "__main__":
    app.run(debug=True)
