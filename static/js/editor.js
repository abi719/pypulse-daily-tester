/**
 * Code Editor Component
 * Implements line numbers, indentation preservation, 4-space tab indentation,
 * auto bracket/quote closing, and run shortcut.
 */

class CodeEditor {
  constructor(textareaId, gutterId) {
    this.textarea = document.getElementById(textareaId);
    this.gutter = document.getElementById(gutterId);
    this.init();
  }

  init() {
    if (!this.textarea || !this.gutter) return;

    // Line numbers update on input and scroll
    this.textarea.addEventListener('input', () => this.updateGutter());
    this.textarea.addEventListener('scroll', () => this.syncScroll());

    // Keyboard handlers
    this.textarea.addEventListener('keydown', (e) => this.handleKeyDown(e));

    this.updateGutter();
  }

  updateGutter() {
    const lines = this.textarea.value.split('\n').length;
    let numbers = '';
    for (let i = 1; i <= Math.max(lines, 1); i++) {
      numbers += `${i}<br>`;
    }
    this.gutter.innerHTML = numbers;
  }

  syncScroll() {
    this.gutter.scrollTop = this.textarea.scrollTop;
  }

  handleKeyDown(e) {
    const start = this.textarea.selectionStart;
    const end = this.textarea.selectionEnd;
    const val = this.textarea.value;

    // Ctrl + Enter or Cmd + Enter to Run Tests
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      if (typeof window.runSampleTestCases === 'function') {
        window.runSampleTestCases();
      }
      return;
    }

    // Tab key: Insert 4 spaces
    if (e.key === 'Tab') {
      e.preventDefault();
      this.textarea.value = val.substring(0, start) + '    ' + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
      this.updateGutter();
      return;
    }

    // Auto-indent on Enter
    if (e.key === 'Enter') {
      e.preventDefault();
      const currentLine = val.substring(0, start).split('\n').pop();
      const match = currentLine.match(/^\s*/);
      let indent = match ? match[0] : '';
      
      // If previous line ends with colon (:), add 4 spaces
      if (currentLine.trim().endsWith(':')) {
        indent += '    ';
      }

      this.textarea.value = val.substring(0, start) + '\n' + indent + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + 1 + indent.length;
      this.updateGutter();
      return;
    }

    // Auto-pair brackets & quotes
    const pairs = {
      '(': ')',
      '[': ']',
      '{': '}',
      '"': '"',
      "'": "'"
    };

    if (pairs[e.key]) {
      e.preventDefault();
      const closeChar = pairs[e.key];
      this.textarea.value = val.substring(0, start) + e.key + closeChar + val.substring(end);
      this.textarea.selectionStart = this.textarea.selectionEnd = start + 1;
      this.updateGutter();
      return;
    }
  }

  getValue() {
    return this.textarea.value;
  }

  setValue(val) {
    this.textarea.value = val || '';
    this.updateGutter();
    this.syncScroll();
  }
}

// Global editor instance
let globalEditor = null;
document.addEventListener('DOMContentLoaded', () => {
  globalEditor = new CodeEditor('code-editor', 'editor-gutter');
});
