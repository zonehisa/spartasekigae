import { SeatingAPI } from './api.js';
import { UIManager } from './ui.js';
import { ScreenshotManager } from './screenshot.js';

class SeatingApp {
  constructor() {
    this.ui = new UIManager();
    this.screenshot = new ScreenshotManager(this.ui.elements.screenshotButton);
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // シャッフルボタン
    this.ui.elements.shuffleButton.addEventListener('click', () => this.handleShuffle());

    // 参加者保存
    this.ui.elements.saveParticipants.addEventListener('click', () => this.handleSaveParticipants());

    // 履歴クリア
    this.ui.elements.clearHistory.addEventListener('click', () => this.handleClearHistory());
  }

  async handleShuffle() {
    try {
      this.setButtonsDisabled(true);
      await this.ui.showShuffleAnimation();

      const newSeating = await SeatingAPI.shuffleSeats();
      this.updateSeats(newSeating);

      setTimeout(() => location.reload(), 500);
    } catch (error) {
      console.error('席替えに失敗しまし���:', error);
      alert(error.message || '席替えに失敗しました。もう一度お試しください。');
    } finally {
      this.setButtonsDisabled(false);
    }
  }

  async handleSaveParticipants() {
    try {
      const newParticipants = this.getParticipantsList();
      await SeatingAPI.updateParticipants(newParticipants);
      alert('参加者リストを更新しました');
      this.ui.hideEditModal();
      location.reload();
    } catch (error) {
      alert(error.message);
    }
  }

  async handleClearHistory() {
    if (!confirm('本当に履歴をクリアしますか？この操作は取り消せません。')) {
      return;
    }

    try {
      await SeatingAPI.clearHistory();
      location.reload();
    } catch (error) {
      alert('履歴のクリアに失敗しました: ' + error.message);
    }
  }

  getParticipantsList() {
    if (this.ui.elements.bulkEdit.style.display === 'none') {
      // 個別入力モード
      const inputs = document.querySelectorAll('.participant-input input');
      return Array.from(inputs).map(input => input.value.trim());
    } else {
      // 一括入力モード
      return this.ui.elements.bulkInput.value
        .split('\n')
        .map(line => line.trim())
        .filter(line => line !== '');
    }
  }

  updateSeats(newSeating) {
    const seats = document.querySelectorAll('.seat');
    newSeating.seats.forEach((member, index) => {
      seats[index].textContent = member;
      if (member) {
        seats[index].style.animation = 'fadeIn 0.5s';
      }
    });
  }

  setButtonsDisabled(disabled) {
    this.ui.elements.shuffleButton.disabled = disabled;
    this.ui.elements.screenshotButton.disabled = disabled;
    this.ui.elements.editButton.disabled = disabled;
  }
}

// アプリケーションの初期化
document.addEventListener('DOMContentLoaded', () => {
  new SeatingApp();
}); 
