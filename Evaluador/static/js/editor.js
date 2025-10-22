// Funcionalidades avanzadas del editor de código
class CodeEditor {
    constructor(textareaId) {
        this.textarea = document.getElementById(textareaId);
        this.initializeEditor();
    }

    initializeEditor() {
        this.addKeyboardShortcuts();
        this.addAutoIndentation();
        this.addBracketMatching();
        this.addLineNumbers();
    }

    addKeyboardShortcuts() {
        this.textarea.addEventListener('keydown', (e) => {
            // Ctrl+S - Guardar
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                document.getElementById('saveBtn').click();
                return;
            }

            // Ctrl+Enter - Ejecutar
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('executeBtn').click();
                return;
            }

            // Ctrl+Shift+F - Formatear
            if (e.ctrlKey && e.shiftKey && e.key === 'F') {
                e.preventDefault();
                document.getElementById('formatBtn').click();
                return;
            }

            // Tab - Indentación
            if (e.key === 'Tab') {
                e.preventDefault();
                this.insertTab();
                return;
            }

            // Shift+Tab - Des-indentar
            if (e.shiftKey && e.key === 'Tab') {
                e.preventDefault();
                this.removeTab();
                return;
            }

            // Enter - Auto indentación
            if (e.key === 'Enter') {
                this.handleEnterKey(e);
                return;
            }

            // Ctrl+/ - Comentar/descomentar
            if (e.ctrlKey && e.key === '/') {
                e.preventDefault();
                this.toggleComment();
                return;
            }
        });
    }

    insertTab() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;

        // Si hay selección, indentar todas las líneas
        if (start !== end) {
            this.indentSelection();
        } else {
            // Insertar 4 espacios
            const newValue = value.substring(0, start) + '    ' + value.substring(end);
            this.textarea.value = newValue;
            this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
        }
    }

    removeTab() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;

        if (start !== end) {
            this.unindentSelection();
        } else {
            // Remover hasta 4 espacios antes del cursor
            const value = this.textarea.value;
            const beforeCursor = value.substring(0, start);
            const match = beforeCursor.match(/( {1,4})$/);
            
            if (match) {
                const spacesToRemove = match[1].length;
                const newValue = value.substring(0, start - spacesToRemove) + value.substring(start);
                this.textarea.value = newValue;
                this.textarea.selectionStart = this.textarea.selectionEnd = start - spacesToRemove;
            }
        }
    }

    indentSelection() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;

        const beforeSelection = value.substring(0, start);
        const selection = value.substring(start, end);
        const afterSelection = value.substring(end);

        // Encontrar el inicio de la primera línea
        const lineStart = beforeSelection.lastIndexOf('\n') + 1;
        const fullSelection = value.substring(lineStart, end);

        // Indentar cada línea
        const indentedLines = fullSelection.split('\n').map(line => {
            return line.length > 0 ? '    ' + line : line;
        }).join('\n');

        const newValue = value.substring(0, lineStart) + indentedLines + afterSelection;
        this.textarea.value = newValue;

        // Mantener selección
        this.textarea.selectionStart = start + 4;
        this.textarea.selectionEnd = end + (indentedLines.length - fullSelection.length);
    }

    unindentSelection() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;

        const beforeSelection = value.substring(0, start);
        const lineStart = beforeSelection.lastIndexOf('\n') + 1;
        const fullSelection = value.substring(lineStart, end);
        const afterSelection = value.substring(end);

        // Des-indentar cada línea
        const unindentedLines = fullSelection.split('\n').map(line => {
            if (line.startsWith('    ')) {
                return line.substring(4);
            } else if (line.startsWith('   ')) {
                return line.substring(3);
            } else if (line.startsWith('  ')) {
                return line.substring(2);
            } else if (line.startsWith(' ')) {
                return line.substring(1);
            }
            return line;
        }).join('\n');

        const newValue = value.substring(0, lineStart) + unindentedLines + afterSelection;
        this.textarea.value = newValue;

        // Ajustar selección
        const removedChars = fullSelection.length - unindentedLines.length;
        this.textarea.selectionStart = Math.max(lineStart, start - 4);
        this.textarea.selectionEnd = end - removedChars;
    }

    handleEnterKey(e) {
        const start = this.textarea.selectionStart;
        const value = this.textarea.value;
        const beforeCursor = value.substring(0, start);
        const currentLine = beforeCursor.split('\n').pop();

        // Detectar indentación de la línea actual
        const indentMatch = currentLine.match(/^(\s*)/);
        let currentIndent = indentMatch ? indentMatch[1] : '';

        // Aumentar indentación si la línea termina con ':'
        if (currentLine.trim().endsWith(':')) {
            currentIndent += '    ';
        }

        // Solo aplicar auto-indentación si hay indentación que aplicar
        if (currentIndent.length > 0) {
            e.preventDefault();
            const newValue = value.substring(0, start) + '\n' + currentIndent + value.substring(start);
            this.textarea.value = newValue;
            this.textarea.selectionStart = this.textarea.selectionEnd = start + 1 + currentIndent.length;
        }
    }

    toggleComment() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;

        // Si no hay selección, comentar/descomentar la línea actual
        if (start === end) {
            this.toggleLineComment(start);
        } else {
            this.toggleSelectionComment(start, end);
        }
    }

    toggleLineComment(position) {
        const value = this.textarea.value;
        const beforeCursor = value.substring(0, position);
        const afterCursor = value.substring(position);
        
        const lineStart = beforeCursor.lastIndexOf('\n') + 1;
        const lineEnd = afterCursor.indexOf('\n');
        const lineEndPos = lineEnd === -1 ? value.length : position + lineEnd;
        
        const line = value.substring(lineStart, lineEndPos);
        const trimmedLine = line.trim();

        let newLine;
        let positionOffset = 0;

        if (trimmedLine.startsWith('# ')) {
            // Descomentar
            newLine = line.replace(/^(\s*)# /, '$1');
            positionOffset = -2;
        } else if (trimmedLine.startsWith('#')) {
            // Descomentar sin espacio
            newLine = line.replace(/^(\s*)#/, '$1');
            positionOffset = -1;
        } else {
            // Comentar
            const indentMatch = line.match(/^(\s*)/);
            const indent = indentMatch ? indentMatch[1] : '';
            newLine = indent + '# ' + line.substring(indent.length);
            positionOffset = 2;
        }

        const newValue = value.substring(0, lineStart) + newLine + value.substring(lineEndPos);
        this.textarea.value = newValue;
        this.textarea.selectionStart = this.textarea.selectionEnd = position + positionOffset;
    }

    toggleSelectionComment(start, end) {
        const value = this.textarea.value;
        const beforeSelection = value.substring(0, start);
        const selection = value.substring(start, end);
        const afterSelection = value.substring(end);

        const lineStart = beforeSelection.lastIndexOf('\n') + 1;
        const fullSelection = value.substring(lineStart, end);

        const lines = fullSelection.split('\n');
        const allCommented = lines.every(line => line.trim() === '' || line.trim().startsWith('#'));

        let newLines;
        let offset = 0;

        if (allCommented) {
            // Descomentar todas las líneas
            newLines = lines.map(line => {
                if (line.trim().startsWith('# ')) {
                    offset -= 2;
                    return line.replace(/^(\s*)# /, '$1');
                } else if (line.trim().startsWith('#')) {
                    offset -= 1;
                    return line.replace(/^(\s*)#/, '$1');
                }
                return line;
            });
        } else {
            // Comentar todas las líneas no vacías
            newLines = lines.map(line => {
                if (line.trim() !== '') {
                    offset += 2;
                    const indentMatch = line.match(/^(\s*)/);
                    const indent = indentMatch ? indentMatch[1] : '';
                    return indent + '# ' + line.substring(indent.length);
                }
                return line;
            });
        }

        const newSelection = newLines.join('\n');
        const newValue = value.substring(0, lineStart) + newSelection + afterSelection;
        this.textarea.value = newValue;

        // Mantener selección
        this.textarea.selectionStart = start;
        this.textarea.selectionEnd = end + offset;
    }

    addBracketMatching() {
        const brackets = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        };

        this.textarea.addEventListener('keydown', (e) => {
            if (brackets[e.key]) {
                const start = this.textarea.selectionStart;
                const end = this.textarea.selectionEnd;

                // Si hay texto seleccionado, envolver con brackets
                if (start !== end) {
                    e.preventDefault();
                    const value = this.textarea.value;
                    const selectedText = value.substring(start, end);
                    const newValue = value.substring(0, start) + e.key + selectedText + brackets[e.key] + value.substring(end);
                    this.textarea.value = newValue;
                    this.textarea.selectionStart = start + 1;
                    this.textarea.selectionEnd = end + 1;
                }
                // Auto-completar brackets para comillas
                else if (e.key === '"' || e.key === "'") {
                    const value = this.textarea.value;
                    const charBefore = value[start - 1];
                    const charAfter = value[start];

                    // Solo auto-completar si no estamos cerrando una comilla
                    if (charAfter !== e.key && charBefore !== '\\') {
                        e.preventDefault();
                        const newValue = value.substring(0, start) + e.key + e.key + value.substring(start);
                        this.textarea.value = newValue;
                        this.textarea.selectionStart = this.textarea.selectionEnd = start + 1;
                    }
                }
                // Auto-completar otros brackets
                else if (e.key !== '"' && e.key !== "'") {
                    e.preventDefault();
                    const value = this.textarea.value;
                    const newValue = value.substring(0, start) + e.key + brackets[e.key] + value.substring(start);
                    this.textarea.value = newValue;
                    this.textarea.selectionStart = this.textarea.selectionEnd = start + 1;
                }
            }
        });
    }

    addLineNumbers() {
        // Esta función podría implementar números de línea visual
        // Por ahora solo actualizamos el contador
        this.textarea.addEventListener('input', () => {
            this.updateLineCount();
        });

        this.textarea.addEventListener('scroll', () => {
            this.syncLineNumbers();
        });
    }

    updateLineCount() {
        const lineCount = this.textarea.value.split('\n').length;
        const lineCountElement = document.getElementById('lineCount');
        if (lineCountElement) {
            lineCountElement.textContent = `Líneas: ${lineCount}`;
        }
    }

    syncLineNumbers() {
        // Sincronizar scroll de números de línea si existe
        const lineNumbersElement = document.querySelector('.line-numbers');
        if (lineNumbersElement) {
            lineNumbersElement.scrollTop = this.textarea.scrollTop;
        }
    }

    // Utilidades públicas
    getCurrentLine() {
        const start = this.textarea.selectionStart;
        const value = this.textarea.value;
        const beforeCursor = value.substring(0, start);
        return beforeCursor.split('\n').length;
    }

    getCurrentColumn() {
        const start = this.textarea.selectionStart;
        const value = this.textarea.value;
        const beforeCursor = value.substring(0, start);
        const currentLine = beforeCursor.split('\n').pop();
        return currentLine.length + 1;
    }

    getSelectedText() {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        return this.textarea.value.substring(start, end);
    }

    insertTextAtCursor(text) {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;
        const newValue = value.substring(0, start) + text + value.substring(end);
        this.textarea.value = newValue;
        this.textarea.selectionStart = this.textarea.selectionEnd = start + text.length;
        this.textarea.focus();
    }

    replaceSelectedText(text) {
        const start = this.textarea.selectionStart;
        const end = this.textarea.selectionEnd;
        const value = this.textarea.value;
        const newValue = value.substring(0, start) + text + value.substring(end);
        this.textarea.value = newValue;
        this.textarea.selectionStart = start;
        this.textarea.selectionEnd = start + text.length;
        this.textarea.focus();
    }
}

// Inicializar editor cuando se carga el DOM
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('codeEditor')) {
        window.codeEditor = new CodeEditor('codeEditor');
    }
});
