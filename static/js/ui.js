import { SeatingAPI } from './api.js';

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
      seatingArea: document.getElementById('seatingArea'),
    };

    this.dragState = {
      sourceElement: null,
      sourceIndex: -1,
    };

    // プレースホルダーとカウンター表示を更新
    this.updateParticipantLimits();
    this.initializeEventListeners();
    this.initializeDragAndDrop();
  }

  updateParticipantLimits() {
    // バルク入力のプレースホルダーを更新
    this.elements.bulkInput.placeholder =
      `参加者名を1行ずつ入力してください（${SeatingAPI.MIN_PARTICIPANTS}～${SeatingAPI.MAX_PARTICIPANTS}名）`;

    // カウンター表示を更新
    const bulkInfo = this.elements.participantCount.parentElement;
    bulkInfo.textContent = bulkInfo.textContent.replace(
      /\d+名/,
      `${SeatingAPI.MIN_PARTICIPANTS}～${SeatingAPI.MAX_PARTICIPANTS}名`
    );
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

    if (lines.length < SeatingAPI.MIN_PARTICIPANTS || lines.length > SeatingAPI.MAX_PARTICIPANTS) {
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

  initializeDragAndDrop() {
    // 席要素にドラッグ＆ドロップイベントを設定
    const seats = this.elements.seatingArea.querySelectorAll('.seat');
    seats.forEach((seat, index) => {
      seat.setAttribute('draggable', 'true');

      seat.addEventListener('dragstart', (e) => {
        if (!seat.textContent.trim()) return;
        this.dragState.sourceElement = seat;
        this.dragState.sourceIndex = index;
        e.dataTransfer.setData('text/plain', seat.textContent);
        seat.classList.add('dragging');
      });

      seat.addEventListener('dragend', () => {
        seat.classList.remove('dragging');
      });

      seat.addEventListener('dragover', (e) => {
        e.preventDefault();
        seat.classList.add('drag-over');
      });

      seat.addEventListener('dragleave', () => {
        seat.classList.remove('drag-over');
      });

      seat.addEventListener('drop', async (e) => {
        e.preventDefault();
        seat.classList.remove('drag-over');

        if (this.dragState.sourceIndex === -1) return;

        try {
          const isSwap = seat.textContent.trim() !== '';
          await SeatingAPI.moveSeat(this.dragState.sourceIndex, index, isSwap);
          location.reload(); // 画面を更新して新しい配置を反映
        } catch (error) {
          alert(error.message);
        }
      });
    });
  }
} 
