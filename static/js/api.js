export class SeatingAPI {
  // 設定情報
  static MIN_PARTICIPANTS = 1;
  static MAX_PARTICIPANTS = 15;

  static async shuffleSeats() {
    const response = await fetch('/shuffle');
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || '席替えに失敗しました');
    }
    return response.json();
  }

  static async updateParticipants(participants) {
    const response = await fetch('/update_participants', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ participants }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    return data;
  }

  static async clearHistory() {
    const response = await fetch('/clear_history', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || '履歴のクリアに失敗しました');
    }
    return data;
  }

  static async moveSeat(fromPos, toPos, isSwap = false) {
    const response = await fetch('/move_seat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ from_pos: fromPos, to_pos: toPos, is_swap: isSwap }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    return data;
  }
} 
