document.addEventListener('DOMContentLoaded', function() {
    const shuffleButton = document.getElementById('shuffleButton');
    const screenshotButton = document.getElementById('screenshotButton');
    const editButton = document.getElementById('editButton');
    const editModal = document.getElementById('editModal');
    const saveParticipants = document.getElementById('saveParticipants');
    const cancelEdit = document.getElementById('cancelEdit');
    const shuffleOverlay = document.getElementById('shuffleOverlay');
    
    // 集モード切り替え要素
    const individualMode = document.getElementById('individualMode');
    const bulkMode = document.getElementById('bulkMode');
    const individualEdit = document.getElementById('individualEdit');
    const bulkEdit = document.getElementById('bulkEdit');
    const bulkInput = document.getElementById('bulkInput');
    const participantCount = document.getElementById('participantCount');
    
    // 編集モード切り替え
    individualMode.addEventListener('click', () => {
        individualMode.classList.add('active');
        bulkMode.classList.remove('active');
        individualEdit.style.display = 'grid';
        bulkEdit.style.display = 'none';
    });
    
    bulkMode.addEventListener('click', () => {
        bulkMode.classList.add('active');
        individualMode.classList.remove('active');
        bulkEdit.style.display = 'block';
        individualEdit.style.display = 'none';
        
        // 現在の参加者リストをテキストエリアに設定
        const inputs = document.querySelectorAll('.participant-input input');
        const currentList = Array.from(inputs).map(input => input.value).join('\n');
        bulkInput.value = currentList;
        updateParticipantCount();
    });
    
    // 参加者数のカウント更新
    function updateParticipantCount() {
        const lines = bulkInput.value.split('\n').filter(line => line.trim() !== '');
        participantCount.textContent = lines.length;
        const bulkInfo = participantCount.parentElement;
        
        if (lines.length !== 15) {
            bulkInfo.classList.add('error');
        } else {
            bulkInfo.classList.remove('error');
        }
    }
    
    // テキストエリアの変更監視
    bulkInput.addEventListener('input', updateParticipantCount);
    
    // シャッフルアニメーションの表示
    function showShuffleAnimation() {
        shuffleOverlay.style.display = 'flex';
        return new Promise(resolve => {
            setTimeout(() => {
                shuffleOverlay.style.display = 'none';
                resolve();
            }, 750 + Math.random() * 100);
        });
    }
    
    // モーダルの表示/非表示
    editButton.addEventListener('click', () => {
        editModal.style.display = 'flex';
    });
    
    cancelEdit.addEventListener('click', () => {
        editModal.style.display = 'none';
    });
    
    // モーダル外クリックで閉じる
    editModal.addEventListener('click', (e) => {
        if (e.target === editModal) {
            editModal.style.display = 'none';
        }
    });
    
    // 参加者リストの保存
    saveParticipants.addEventListener('click', async () => {
        let newParticipants;
        
        if (bulkEdit.style.display === 'none') {
            // 個別入力モード
            const inputs = document.querySelectorAll('.participant-input input');
            newParticipants = Array.from(inputs).map(input => input.value.trim());
        } else {
            // 一括入力モード
            newParticipants = bulkInput.value.split('\n')
                .map(line => line.trim())
                .filter(line => line !== '');
        }
        
        try {
            const response = await fetch('/update_participants', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ participants: newParticipants }),
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error);
            }
            
            alert(data.message);
            editModal.style.display = 'none';
            location.reload();
        } catch (error) {
            alert(error.message);
        }
    });
    
    // シャッフルボタンのクリックイベント
    shuffleButton.addEventListener('click', async function() {
        try {
            shuffleButton.disabled = true;
            screenshotButton.disabled = true;
            editButton.disabled = true;
            
            await showShuffleAnimation();
            
            const response = await fetch('/shuffle');
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || '席替えに失敗しました');
            }
            
            const newSeating = await response.json();
            
            const seats = document.querySelectorAll('.seat');
            
            newSeating.seats.forEach((member, index) => {
                seats[index].textContent = member;
                if (member) {
                    seats[index].style.animation = 'fadeIn 0.5s';
                }
            });

            // アニメーション完了後にページをリロード
            setTimeout(() => {
                location.reload();
            }, 500);
        } catch (error) {
            console.error('席替えに失敗しました:', error);
            alert(error.message || '席替えに失敗しました。もう一度お試しください。');
        } finally {
            shuffleButton.disabled = false;
            screenshotButton.disabled = false;
            editButton.disabled = false;
        }
    });
    
    // スクリーンショットボタンのクリックイベント
    screenshotButton.addEventListener('click', async function() {
        try {
            screenshotButton.disabled = true;
            const originalText = screenshotButton.textContent;
            screenshotButton.textContent = 'コピー中...';
            
            // モーダルとオーバーレイを非表示に
            editModal.style.display = 'none';
            shuffleOverlay.style.display = 'none';
            
            // ボタンを一時的に非表示
            const buttonContainer = document.querySelector('.button-container');
            buttonContainer.style.display = 'none';
            
            // タイトルを一時的に非表示
            const title = document.querySelector('h1');
            title.style.display = 'none';

            // スクリーンショットの生成
            const seatingGrid = document.querySelector('.seating-grid');
            const canvas = await html2canvas(seatingGrid, {
                scale: 2,
                backgroundColor: '#ffffff'
            });
            
            // 元の表示状態に戻す
            buttonContainer.style.display = 'flex';
            title.style.display = 'block';
            
            canvas.toBlob(async function(blob) {
                try {
                    const clipboardItem = new ClipboardItem({ 'image/png': blob });
                    await navigator.clipboard.write([clipboardItem]);
                    screenshotButton.textContent = 'コピー完了！';
                    setTimeout(() => {
                        screenshotButton.textContent = originalText;
                    }, 2000);
                } catch (error) {
                    console.error('クリップボードへのコピーに失��:', error);
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `seating_${new Date().toISOString().slice(0,19).replace(/[:-]/g, '')}.png`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    alert('クリップボードへのコピーに失敗しました。代わりに画像をダウンロードしました。');
                }
            }, 'image/png', 1.0);
        } catch (error) {
            console.error('キャプチャに失敗しました:', error);
            alert('キャプチャに失敗しました。もう一度お試しください。');
        } finally {
            screenshotButton.disabled = false;
        }
    });
    
    // 履歴モーダル関連の要素
    const historyButton = document.getElementById('historyButton');
    const historyModal = document.getElementById('historyModal');
    const closeHistory = document.getElementById('closeHistory');

    // 履歴モーダルの表示
    historyButton.addEventListener('click', () => {
        historyModal.style.display = 'block';
    });

    // 履歴モーダル��閉じる
    closeHistory.addEventListener('click', () => {
        historyModal.style.display = 'none';
    });

    // モーダルの外側をクリックして閉じる
    window.addEventListener('click', (event) => {
        if (event.target === historyModal) {
            historyModal.style.display = 'none';
        }
    });

    // 履歴クリアボタンのイベントリスナー
    const clearHistory = document.getElementById('clearHistory');

    clearHistory.addEventListener('click', async () => {
        // 確認ダイアログを表示
        if (!confirm('本当に履歴をクリアしますか？この操作は取り消せません。')) {
            return;
        }

        try {
            const response = await fetch('/clear_history', {
                method: 'POST',
            });
            const data = await response.json();

            if (response.ok) {
                // 履歴リストを空にする
                const historyList = document.querySelector('.history-list');
                historyList.innerHTML = '';
                alert('履歴をクリアしました');
            } else {
                alert('エラー: ' + data.error);
            }
        } catch (error) {
            alert('エラーが発生しました: ' + error);
        }
    });
}); 

