// Cliente API para comunicación con el backend
class ApiClient {
    constructor() {
        this.baseUrl = window.location.origin;
        this.timeout = 10000; // 10 segundos
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            timeout: this.timeout,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await Promise.race([
                fetch(url, config),
                new Promise((_, reject) => 
                    setTimeout(() => reject(new Error('Timeout')), this.timeout)
                )
            ]);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            return { 
                success: false, 
                error: error.message || 'Error de conexión' 
            };
        }
    }

    async evaluarCodigo(codigo) {
        return await this.makeRequest('/api/evaluar', {
            method: 'POST',
            body: JSON.stringify({ codigo })
        });
    }

    async ejecutarCodigo(codigo) {
        return await this.makeRequest('/api/ejecutar', {
            method: 'POST',
            body: JSON.stringify({ codigo })
        });
    }

    async obtenerEjemplos() {
        return await this.makeRequest('/api/ejemplos');
    }

    // Utilidad para verificar conectividad
    async checkConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/api/ejemplos`, {
                method: 'HEAD',
                timeout: 5000
            });
            return response.ok;
        } catch {
            return false;
        }
    }

    // Retry logic para requests fallidos
    async makeRequestWithRetry(endpoint, options = {}, maxRetries = 3) {
        let lastError;
        
        for (let i = 0; i <= maxRetries; i++) {
            const result = await this.makeRequest(endpoint, options);
            
            if (result.success) {
                return result;
            }
            
            lastError = result.error;
            
            // No hacer retry en errores de cliente (4xx)
            if (result.error && result.error.includes('HTTP 4')) {
                break;
            }
            
            // Esperar antes del próximo intento
            if (i < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
            }
        }
        
        return { success: false, error: lastError };
    }
}

// Instancia global del cliente API
window.apiClient = new ApiClient();
