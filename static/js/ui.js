export class UIManager {
  constructor() {
    this.elements = {
      shuffleButton: document.getElementById('shuffleButton'),
      screenshotButton: document.getElementById('screenshotButton'),
      editButton: document.getElementById('editButton'),
      editModal: document.getElementById('editModal'),
      saveParticipants: document.getElementById('saveParticipants'),
      cancelEdit: document.getElementById('cancelEdit'),
      shuffleOverlay: document.getElementById('shuffleOverlay'),
      individualMode: document.getElementById('individualMode'),
      bulkMode: document.getElementById('bulkMode'),
      individualEdit: document.getElementById('individualEdit'),
      bulkEdit: document.getElementById('bulkEdit'),
      bulkInput: document.getElementById('bulkInput'),
      participantCount: document.getElementById('participantCount'),
      historyButton: document.getElementById('historyButton'),
      historyModal: document.getElementById('historyModal'),
      closeHistory: document.getElementById('closeHistory'),
      clearHistory: document.getElementById('clearHistory'),
    };
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    // 編集モード切り替え
    this.elements.individualMode.addEventListener('click', () => this.switchToIndividualMode());
    this.elements.bulkMode.addEventListener('click', () => this.switchToBulkMode());

    // モーダル制御
    this.elements.editButton.addEventListener('click', () => this.showEditModal());
    this.elements.cancelEdit.addEventListener('click', () => this.hideEditModal());
    this.elements.historyButton.addEventListener('click', () => this.showHistoryModal());
    this.elements.closeHistory.addEventListener('click', () => this.hideHistoryModal());

    // モーダル外クリックでの閉じる
    this.elements.editModal.addEventListener('click', (e) => {
      if (e.target === this.elements.editModal) this.hideEditModal();
    });
    this.elements.historyModal.addEventListener('click', (e) => {
      if (e.target === this.elements.historyModal) this.hideHistoryModal();
    });

    // バルク入力の監視
    this.elements.bulkInput.addEventListener('input', () => this.updateParticipantCount());
  }

  switchToIndividualMode() {
    this.elements.individualMode.classList.add('active');
    this.elements.bulkMode.classList.remove('active');
    this.elements.individualEdit.style.display = 'grid';
    this.elements.bulkEdit.style.display = 'none';
  }

  switchToBulkMode() {
    this.elements.bulkMode.classList.add('active');
    this.elements.individualMode.classList.remove('active');
    this.elements.bulkEdit.style.display = 'block';
    this.elements.individualEdit.style.display = 'none';

    const inputs = document.querySelectorAll('.participant-input input');
    const currentList = Array.from(inputs).map(input => input.value).join('\n');
    this.elements.bulkInput.value = currentList;
    this.updateParticipantCount();
  }

  updateParticipantCount() {
    const lines = this.elements.bulkInput.value.split('\n').filter(line => line.trim() !== '');
    this.elements.participantCount.textContent = lines.length;
    const bulkInfo = this.elements.participantCount.parentElement;

    if (lines.length !== 15) {
      bulkInfo.classList.add('error');
    } else {
      bulkInfo.classList.remove('error');
    }
  }

  showEditModal() {
    this.elements.editModal.style.display = 'flex';
  }

  hideEditModal() {
    this.elements.editModal.style.display = 'none';
  }

  showHistoryModal() {
    this.elements.historyModal.style.display = 'block';
  }

  hideHistoryModal() {
    this.elements.historyModal.style.display = 'none';
  }

  async showShuffleAnimation() {
    this.elements.shuffleOverlay.style.display = 'flex';
    await new Promise(resolve => {
      setTimeout(() => {
        this.elements.shuffleOverlay.style.display = 'none';
        resolve();
      }, 750 + Math.random() * 100);
    });
  }
} 
