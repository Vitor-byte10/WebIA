// Controlador principal de la aplicación
class EvaluadorApp {
    constructor() {
        this.isAnalyzing = false;
        this.currentCode = '';
        this.initializeApp();
    }

    initializeApp() {
        this.initializeElements();
        this.bindEvents();
        this.loadExamples();
        this.updateStats();
    }

    initializeElements() {
        // Editor
        this.codeEditor = document.getElementById('codeEditor');
        this.lineCount = document.getElementById('lineCount');
        this.charCount = document.getElementById('charCount');
        
        // Botones principales
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.executeBtn = document.getElementById('executeBtn');
        this.formatBtn = document.getElementById('formatBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.saveBtn = document.getElementById('saveBtn');
        
        // Upload
        this.fileDropZone = document.getElementById('fileDropZone');
        this.fileInput = document.getElementById('fileInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeFile = document.getElementById('removeFile');
        
        // Métricas
        this.linesMetric = document.getElementById('linesMetric');
        this.functionsMetric = document.getElementById('functionsMetric');
        this.classesMetric = document.getElementById('classesMetric');
        this.complexityMetric = document.getElementById('complexityMetric');
        
        // Calidad
        this.qualityFill = document.getElementById('qualityFill');
        this.qualityPercentage = document.getElementById('qualityPercentage');
        this.qualityText = document.getElementById('qualityText');
        
        // Feedback y sugerencias
        this.feedbackContainer = document.getElementById('feedbackContainer');
        this.suggestionsContainer = document.getElementById('suggestionsContainer');
        
        // Estado y resultados
        this.analysisStatus = document.getElementById('analysisStatus');
        this.executionResult = document.getElementById('executionResult');
        this.toastContainer = document.getElementById('toastContainer');
    }

    bindEvents() {
        // Editor events
        this.codeEditor.addEventListener('input', () => {
            this.updateStats();
            this.currentCode = this.codeEditor.value;
        });

        // Botones principales
        this.analyzeBtn.addEventListener('click', () => this.analyzeCode());
        this.executeBtn.addEventListener('click', () => this.executeCode());
        this.formatBtn.addEventListener('click', () => this.formatCode());
        this.clearBtn.addEventListener('click', () => this.clearEditor());
        this.saveBtn.addEventListener('click', () => this.saveCode());

        // File upload events
        this.fileDropZone.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.removeFile.addEventListener('click', () => this.removeFileHandler());

        // Drag and drop
        this.fileDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.fileDropZone.classList.add('drag-over');
        });

        this.fileDropZone.addEventListener('dragleave', () => {
            this.fileDropZone.classList.remove('drag-over');
        });

        this.fileDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.fileDropZone.classList.remove('drag-over');
            this.handleFileDrop(e);
        });

        // Ejemplos
        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const exampleType = e.currentTarget.dataset.example;
                this.loadExample(exampleType);
            });
        });
    }

    updateStats() {
        const code = this.codeEditor.value;
        const lines = code.split('\n').length;
        const chars = code.length;
        
        this.lineCount.textContent = `Líneas: ${lines}`;
        this.charCount.textContent = `Caracteres: ${chars}`;
        
        // Actualizar métricas básicas
        this.linesMetric.textContent = lines;
    }

    async analyzeCode() {
        if (this.isAnalyzing) return;
        
        const code = this.codeEditor.value.trim();
        if (!code) {
            this.showToast('Escribe código para analizar', 'error');
            return;
        }

        this.setAnalyzing(true);
        
        try {
            const response = await fetch('/api/evaluar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ codigo: code })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showToast(data.error, 'error');
            } else {
                this.displayResults(data);
                this.showToast('Análisis completado', 'success');
            }
        } catch (error) {
            console.error('Error analyzing code:', error);
            this.showToast('Error al analizar código', 'error');
        } finally {
            this.setAnalyzing(false);
        }
    }

    async executeCode() {
        const code = this.codeEditor.value.trim();
        if (!code) {
            this.showToast('Escribe código para ejecutar', 'error');
            return;
        }

        try {
            const response = await fetch('/api/ejecutar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ codigo: code })
            });

            const data = await response.json();
            this.showExecutionResult(data);
            
            if (data.success) {
                this.showToast('Código ejecutado', 'success');
            } else {
                this.showToast('Error en ejecución', 'error');
            }
        } catch (error) {
            console.error('Error executing code:', error);
            this.showToast('Error al ejecutar código', 'error');
        }
    }

    formatCode() {
        const code = this.codeEditor.value;
        if (!code.trim()) {
            this.showToast('No hay código para formatear', 'error');
            return;
        }

        // Formateo básico de Python
        const lines = code.split('\n');
        const formatted = lines.map(line => {
            // Remover espacios extra al final
            line = line.trimEnd();
            
            // Formateo básico de indentación
            if (line.trim().startsWith('#')) {
                return line; // Mantener comentarios como están
            }
            
            return line;
        }).join('\n');

        this.codeEditor.value = formatted;
        this.updateStats();
        this.showToast('Código formateado', 'info');
    }

    clearEditor() {
        if (this.codeEditor.value.trim() === '') {
            this.showToast('El editor ya está vacío', 'info');
            return;
        }

        if (confirm('¿Estás seguro de que quieres limpiar el editor?')) {
            this.codeEditor.value = '';
            this.updateStats();
            this.resetResults();
            this.showToast('Editor limpiado', 'info');
        }
    }

    saveCode() {
        const code = this.codeEditor.value;
        if (!code.trim()) {
            this.showToast('No hay código para guardar', 'error');
            return;
        }

        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'codigo.py';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('Código guardado', 'success');
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.loadFile(file);
        }
    }

    handleFileDrop(event) {
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.loadFile(files[0]);
        }
    }

    loadFile(file) {
        if (!file.name.endsWith('.py') && !file.name.endsWith('.txt')) {
            this.showToast('Solo se permiten archivos .py o .txt', 'error');
            return;
        }

        if (file.size > 1024 * 1024) { // 1MB límite
            this.showToast('Archivo muy grande (máximo 1MB)', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.codeEditor.value = e.target.result;
            this.updateStats();
            this.showFileInfo(file);
            this.showToast(`Archivo "${file.name}" cargado`, 'success');
        };
        reader.onerror = () => {
            this.showToast('Error al leer el archivo', 'error');
        };
        reader.readAsText(file);
    }

    showFileInfo(file) {
        this.fileName.textContent = file.name;
        this.fileSize.textContent = `${(file.size / 1024).toFixed(1)} KB`;
        this.fileInfo.style.display = 'block';
        this.fileDropZone.style.display = 'none';
    }

    removeFileHandler() {
        this.fileInfo.style.display = 'none';
        this.fileDropZone.style.display = 'block';
        this.fileInput.value = '';
        this.showToast('Archivo removido', 'info');
    }

    async loadExamples() {
        try {
            const response = await fetch('/api/ejemplos');
            const ejemplos = await response.json();
            window.ejemplos = ejemplos; // Guardar para uso posterior
        } catch (error) {
            console.error('Error loading examples:', error);
        }
    }

    loadExample(type) {
        if (!window.ejemplos || !window.ejemplos[type]) {
            this.showToast('Error cargando ejemplo', 'error');
            return;
        }

        this.codeEditor.value = window.ejemplos[type];
        this.updateStats();
        this.showToast(`Ejemplo "${type}" cargado`, 'success');
    }

    setAnalyzing(analyzing) {
        this.isAnalyzing = analyzing;
        
        if (analyzing) {
            this.analyzeBtn.disabled = true;
            this.analyzeBtn.innerHTML = '<span class="spinner"></span> Analizando...';
            this.analysisStatus.style.display = 'flex';
        } else {
            this.analyzeBtn.disabled = false;
            this.analyzeBtn.innerHTML = '<span class="btn-icon">🔍</span> Analizar Código';
            this.analysisStatus.style.display = 'none';
        }
    }

    displayResults(data) {
        // Actualizar métricas
        if (data.metricas) {
            this.linesMetric.textContent = data.metricas.lineas_codigo || 0;
            this.functionsMetric.textContent = data.metricas.funciones || 0;
            this.classesMetric.textContent = data.metricas.clases || 0;
            this.complexityMetric.textContent = data.metricas.complejidad || 0;
        }

        // Actualizar calidad
        const score = data.score || 0;
        this.qualityFill.style.width = `${score}%`;
        this.qualityPercentage.textContent = `${score}%`;
        
        // Texto de calidad según score
        let qualityMessage = '';
        if (score >= 90) qualityMessage = 'Excelente calidad de código';
        else if (score >= 70) qualityMessage = 'Buena calidad de código';
        else if (score >= 50) qualityMessage = 'Calidad moderada';
        else if (score >= 30) qualityMessage = 'Necesita mejoras';
        else qualityMessage = 'Requiere trabajo significativo';
        
        this.qualityText.textContent = qualityMessage;

        // Mostrar feedback
        this.displayFeedback(data.feedback || []);
        
        // Mostrar sugerencias
        this.displaySugerencias(data.sugerencias || []);
    }

    displayFeedback(feedback) {
        if (!feedback.length) {
            this.feedbackContainer.innerHTML = `
                <div class="feedback-item feedback-info">
                    <span class="feedback-icon">ℹ️</span>
                    <div class="feedback-content">
                        <div class="feedback-message">No hay feedback disponible</div>
                    </div>
                </div>
            `;
            return;
        }

        this.feedbackContainer.innerHTML = feedback.map(item => {
            const typeClass = `feedback-${item.tipo}`;
            const icon = this.getFeedbackIcon(item.tipo);
            
            return `
                <div class="feedback-item ${typeClass}">
                    <span class="feedback-icon">${icon}</span>
                    <div class="feedback-content">
                        <div class="feedback-message">${item.mensaje}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    displaySugerencias(sugerencias) {
        if (!sugerencias.length) {
            this.suggestionsContainer.innerHTML = `
                <div class="suggestion-item">
                    <span class="suggestion-icon">💡</span>
                    <span>No hay sugerencias adicionales</span>
                </div>
            `;
            return;
        }

        this.suggestionsContainer.innerHTML = sugerencias.map(sugerencia => `
            <div class="suggestion-item">
                <span class="suggestion-icon">💡</span>
                <span>${sugerencia}</span>
            </div>
        `).join('');
    }

    getFeedbackIcon(tipo) {
        const icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': 'ℹ️'
        };
        return icons[tipo] || 'ℹ️';
    }

    showExecutionResult(data) {
        this.executionResult.style.display = 'block';
        
        if (data.success) {
            this.executionResult.innerHTML = `<div style="color: #10b981; margin-bottom: 0.5rem;">✅ Ejecución exitosa:</div>${data.output}`;
        } else {
            this.executionResult.innerHTML = `<div style="color: #ef4444; margin-bottom: 0.5rem;">❌ Error:</div>${data.error}`;
        }
        
        // Auto-hide después de 10 segundos
        setTimeout(() => {
            this.executionResult.style.display = 'none';
        }, 10000);
    }

    resetResults() {
        // Resetear métricas
        this.linesMetric.textContent = '0';
        this.functionsMetric.textContent = '0';
        this.classesMetric.textContent = '0';
        this.complexityMetric.textContent = '0';
        
        // Resetear calidad
        this.qualityFill.style.width = '0%';
        this.qualityPercentage.textContent = '0%';
        this.qualityText.textContent = 'Esperando análisis...';
        
        // Resetear feedback
        this.feedbackContainer.innerHTML = `
            <div class="feedback-item feedback-info">
                <span class="feedback-icon">ℹ️</span>
                <div class="feedback-content">
                    <div class="feedback-message">
                        Escribe código o carga un archivo .py para obtener feedback detallado
                    </div>
                </div>
            </div>
        `;
        
        // Resetear sugerencias
        this.suggestionsContainer.innerHTML = `
            <div class="suggestion-item">
                <span class="suggestion-icon">💡</span>
                <span>Usa nombres descriptivos para variables y funciones</span>
            </div>
            <div class="suggestion-item">
                <span class="suggestion-icon">💡</span>
                <span>Agrega docstrings para documentar tu código</span>
            </div>
            <div class="suggestion-item">
                <span class="suggestion-icon">💡</span>
                <span>Implementa manejo de errores con try/except</span>
            </div>
        `;
        
        // Ocultar resultado de ejecución
        this.executionResult.style.display = 'none';
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Mostrar toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Ocultar y remover toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new EvaluadorApp();
});

// Utilidades globales
window.EvaluadorUtils = {
    // Formatear tamaño de archivo
    formatFileSize: (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    },
    
    // Validar código Python básico
    isValidPython: (code) => {
        // Verificaciones básicas de sintaxis Python
        const lines = code.split('\n');
        let indentStack = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmedLine = line.trim();
            
            // Ignorar líneas vacías y comentarios
            if (!trimmedLine || trimmedLine.startsWith('#')) continue;
            
            // Contar espacios de indentación
            const indent = line.length - line.trimLeft().length;
            
            // Verificar caracteres inválidos básicos
            if (line.includes('\t') && line.includes('    ')) {
                return { valid: false, error: `Línea ${i+1}: Mezcla de tabs y espacios` };
            }
        }
        
        return { valid: true };
    },
    
    // Detectar lenguaje de programación
    detectLanguage: (code) => {
        const pythonKeywords = ['def ', 'class ', 'import ', 'from ', 'print(', 'if __name__'];
        const pythonScore = pythonKeywords.reduce((score, keyword) => {
            return score + (code.includes(keyword) ? 1 : 0);
        }, 0);
        
        return pythonScore > 0 ? 'python' : 'unknown';
    }
};
