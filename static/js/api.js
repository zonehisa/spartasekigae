export class SeatingAPI {
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
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error);
    }
    return data;
  }
} 
