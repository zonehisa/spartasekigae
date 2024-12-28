export class ScreenshotManager {
  constructor(button) {
    this.button = button;
    this.button.addEventListener('click', () => this.handleScreenshot());
  }

  async handleScreenshot() {
    try {
      this.button.disabled = true;
      const originalText = this.button.textContent;
      this.button.textContent = 'コピー中...';

      // UI要素の一時的な非表示
      this.hideUIElements();

      // スクリーンショットの生成
      const seatingGrid = document.querySelector('.seating-grid');
      const canvas = await html2canvas(seatingGrid, {
        scale: 2,
        backgroundColor: '#ffffff'
      });

      // UI要素の表示を復元
      this.showUIElements();

      await this.copyToClipboard(canvas, originalText);
    } catch (error) {
      console.error('キャプチャに失敗しました:', error);
      alert('キャプチャに失敗しました。もう一度お試しください。');
    } finally {
      this.button.disabled = false;
    }
  }

  hideUIElements() {
    document.querySelector('.button-container').style.display = 'none';
    document.querySelector('h1').style.display = 'none';
    document.getElementById('editModal').style.display = 'none';
    document.getElementById('shuffleOverlay').style.display = 'none';
  }

  showUIElements() {
    document.querySelector('.button-container').style.display = 'flex';
    document.querySelector('h1').style.display = 'block';
  }

  async copyToClipboard(canvas, originalText) {
    canvas.toBlob(async blob => {
      try {
        const clipboardItem = new ClipboardItem({ 'image/png': blob });
        await navigator.clipboard.write([clipboardItem]);
        this.button.textContent = 'コピー完了！';
        setTimeout(() => {
          this.button.textContent = originalText;
        }, 2000);
      } catch (error) {
        console.error('クリップボードへのコピーに失敗:', error);
        this.downloadImage(blob);
      }
    }, 'image/png', 1.0);
  }

  downloadImage(blob) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `seating_${new Date().toISOString().slice(0, 19).replace(/[:-]/g, '')}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    alert('クリップボードへのコピーに失敗しました。代わりに画像をダウンロードしました。');
  }
} 
