// Gestión de ejemplos de código
class ExamplesManager {
    constructor() {
        this.examples = {};
        this.loadExamplesFromServer();
    }

    async loadExamplesFromServer() {
        try {
            const response = await fetch('/api/ejemplos');
            if (response.ok) {
                this.examples = await response.json();
            } else {
                // Fallback a ejemplos locales si el servidor no responde
                this.loadLocalExamples();
            }
        } catch (error) {
            console.log('Cargando ejemplos locales...');
            this.loadLocalExamples();
        }
    }

    loadLocalExamples() {
        this.examples = {
            basic: `def calcular_factorial(n):
    """
    Calcula el factorial de un número entero positivo
    """
    if n < 0:
        raise ValueError("El número debe ser positivo")
    elif n <= 1:
        return 1
    else:
        return n * calcular_factorial(n - 1)

# Ejemplo de uso
try:
    numero = 5
    resultado = calcular_factorial(numero)
    print(f"El factorial de {numero} es {resultado}")
except ValueError as e:
    print(f"Error: {e}")`,

            loop: `# Análisis de datos con bucles y condicionales
import random

def analizar_ventas():
    """Analiza las ventas mensuales y calcula estadísticas"""
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    ventas = [random.randint(1000, 5000) for _ in range(len(meses))]
    
    total_ventas = sum(ventas)
    promedio = total_ventas / len(meses)
    max_ventas = max(ventas)
    min_ventas = min(ventas)
    
    print("📊 REPORTE DE VENTAS")
    print("-" * 30)
    
    for i, (mes, venta) in enumerate(zip(meses, ventas)):
        indicador = "📈" if venta > promedio else "📉"
        print(f"{mes}: ${venta:,} {indicador}")
    
    print("-" * 30)
    print(f"Total: ${total_ventas:,}")
    print(f"Promedio: ${promedio:,.2f}")
    print(f"Máximo: ${max_ventas:,}")
    print(f"Mínimo: ${min_ventas:,}")
    
    return {
        'total': total_ventas,
        'promedio': promedio,
        'maximo': max_ventas,
        'minimo': min_ventas
    }

            loop: `# Análisis de datos con bucles y condicionales
import random

def analizar_ventas():
    """Analiza las ventas mensuales y calcula estadísticas"""
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    ventas = [random.randint(1000, 5000) for _ in range(len(meses))]
    
    total_ventas = sum(ventas)
    promedio = total_ventas / len(meses)
    max_ventas = max(ventas)
    min_ventas = min(ventas)
    
    print("📊 REPORTE DE VENTAS")
    print("-" * 30)
    
    for i, (mes, venta) in enumerate(zip(meses, ventas)):
        indicador = "📈" if venta > promedio else "📉"
        print(f"{mes}: ${venta:,} {indicador}")
    
    print("-" * 30)
    print(f"Total: ${total_ventas:,}")
    print(f"Promedio: ${promedio:,.2f}")
    print(f"Máximo: ${max_ventas:,}")
    print(f"Mínimo: ${min_ventas:,}")
    
    return {
        'total': total_ventas,
        'promedio': promedio,
        'maximo': max_ventas,
        'minimo': min_ventas
    }

# Ejecutar análisis
resultado = analizar_ventas()`,

            class: `class GestorInventario:
    """Sistema de gestión de inventario para una tienda"""

    def __init__(self):
        self.productos = {}
        self.historial = []

    def agregar_producto(self, nombre, precio, stock=0):
        """Agrega un producto al inventario"""
        if nombre in self.productos:
            print(f"⚠️ El producto {nombre} ya existe. Actualizando...")
        
        self.productos[nombre] = {
            "precio": precio, 
            "stock": stock,
            "fecha_agregado": "2024-01-01"
        }
        
        self.historial.append(f"Agregado: {nombre}")
        print(f"✅ Producto {nombre} agregado correctamente")

    def vender_producto(self, nombre, cantidad=1):
        """Vende una cantidad específica de un producto"""
        if nombre not in self.productos:
            print(f"❌ Error: Producto {nombre} no encontrado")
            return False
        
        if self.productos[nombre]["stock"] < cantidad:
            print(f"❌ Stock insuficiente para {nombre}")
            return False
        
        self.productos[nombre]["stock"] -= cantidad
        self.historial.append(f"Vendido: {cantidad}x {nombre}")
        print(f"💰 Vendido: {cantidad}x {nombre}")
        return True

    def mostrar_inventario(self):
        """Muestra todos los productos con su información"""
        if not self.productos:
            print("📦 Inventario vacío")
            return
        
        print("📋 INVENTARIO ACTUAL")
        print("=" * 50)
        
        total_valor = 0
        for nombre, datos in self.productos.items():
            valor_stock = datos['precio'] * datos['stock']
            total_valor += valor_stock
            
            # Indicador de stock
            if datos['stock'] == 0:
                indicador = "🔴"
            elif datos['stock'] < 5:
                indicador = "🟡"
            else:
                indicador = "🟢"
            
            print(f"{indicador} {nombre}:")
            print(f"   Precio: ${datos['precio']:,.2f}")
            print(f"   Stock: {datos['stock']} unidades")
            print(f"   Valor total: ${valor_stock:,.2f}")
            print("-" * 30)
        
        print(f"💎 VALOR TOTAL DEL INVENTARIO: ${total_valor:,.2f}")

    def productos_bajo_stock(self, limite=5):
        """Encuentra productos con stock bajo"""
        bajo_stock = []
        for nombre, datos in self.productos.items():
            if datos['stock'] <= limite:
                bajo_stock.append((nombre, datos['stock']))
        
        if bajo_stock:
            print("⚠️ PRODUCTOS CON STOCK BAJO:")
            for producto, cantidad in bajo_stock:
                print(f"   - {producto}: {cantidad} unidades")
        else:
            print("✅ Todos los productos tienen stock suficiente")
        
        return bajo_stock

    def mostrar_historial(self):
        """Muestra el historial de operaciones"""
        print("📈 HISTORIAL DE OPERACIONES:")
        for i, operacion in enumerate(self.historial[-10:], 1):
            print(f"  {i}. {operacion}")

# Demostración del sistema
print("🏪 Iniciando sistema de inventario...")
inventario = GestorInventario()

# Agregar productos
inventario.agregar_producto("Laptop Gaming", 1200, 15)
inventario.agregar_producto("Mouse Inalámbrico", 25, 50)
inventario.agregar_producto("Teclado Mecánico", 80, 3)
inventario.agregar_producto("Monitor 4K", 300, 8)

# Realizar algunas ventas
inventario.vender_producto("Laptop Gaming", 2)
inventario.vender_producto("Mouse Inalámbrico", 10)

# Mostrar estado actual
print("\n")
inventario.mostrar_inventario()
print("\n")
inventario.productos_bajo_stock()
print("\n")
inventario.mostrar_historial()`
        };
    }

    getExample(type) {
        return this.examples[type] || null;
    }

    getAllExamples() {
        return this.examples;
    }

    getExampleInfo(type) {
        const info = {
            basic: {
                title: "Función Básica",
                description: "Ejemplo de función con manejo de errores y recursión",
                difficulty: "Principiante",
                concepts: ["Funciones", "Recursión", "Manejo de errores", "Documentación"]
            },
            loop: {
                title: "Bucles y Lógica",
                description: "Análisis de datos usando bucles, condicionales y estructuras",
                difficulty: "Intermedio",
                concepts: ["Bucles", "Condicionales", "Listas", "Diccionarios", "f-strings"]
            },
            class: {
                title: "Programación OOP",
                description: "Sistema completo con clases, métodos y gestión de estado",
                difficulty: "Avanzado",
                concepts: ["Clases", "Métodos", "Atributos", "Encapsulación", "Gestión de estado"]
            }
        };
        
        return info[type] || null;
    }

    // Cargar ejemplo en el editor
    loadExample(type, editorId = 'codeEditor') {
        const example = this.getExample(type);
        const editor = document.getElementById(editorId);
        
        if (example && editor) {
            editor.value = example;
            
            // Disparar evento de cambio para actualizar estadísticas
            const event = new Event('input', { bubbles: true });
            editor.dispatchEvent(event);
            
            // Mostrar información del ejemplo
            this.showExampleInfo(type);
            
            return true;
        }
        
        return false;
    }

    showExampleInfo(type) {
        const info = this.getExampleInfo(type);
        if (!info) return;

        // Crear toast informativo
        const toast = document.createElement('div');
        toast.className = 'toast toast-info';
        toast.innerHTML = `
            <strong>${info.title}</strong><br>
            ${info.description}<br>
            <small>Dificultad: ${info.difficulty}</small>
        `;

        const container = document.getElementById('toastContainer');
        if (container) {
            container.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 100);
            
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.parentNode.removeChild(toast);
                    }
                }, 300);
            }, 4000);
        }
    }

    // Generar ejemplo personalizado
    generateCustomExample(concepts = []) {
        let example = '# Ejemplo personalizado\n';
        
        if (concepts.includes('variables')) {
            example += `
# Variables y tipos de datos
nombre = "Python"
version = 3.9
activo = True

print(f"Lenguaje: {nombre}")
print(f"Versión: {version}")
print(f"Activo: {activo}")
`;
        }
        
        if (concepts.includes('funciones')) {
            example += `
def saludar(nombre, edad=None):
    """Función que saluda a una persona"""
    saludo = f"Hola, {nombre}!"
    if edad:
        saludo += f" Tienes {edad} años."
    return saludo

# Uso de la función
mensaje = saludar("Ana", 25)
print(mensaje)
`;
        }
        
        if (concepts.includes('listas')) {
            example += `
# Trabajo con listas
numeros = [1, 2, 3, 4, 5]
frutas = ["manzana", "banana", "naranja"]

# Operaciones con listas
print(f"Números: {numeros}")
print(f"Suma total: {sum(numeros)}")
print(f"Frutas disponibles: {len(frutas)}")

# Agregar elementos
frutas.append("uva")
print(f"Frutas actualizadas: {frutas}")
`;
        }
        
        if (concepts.includes('diccionarios')) {
            example += `
# Diccionarios
estudiante = {
    "nombre": "Carlos",
    "edad": 20,
    "carrera": "Ingeniería",
    "materias": ["Matemáticas", "Física", "Programación"]
}

print(f"Estudiante: {estudiante['nombre']}")
print(f"Materias: {', '.join(estudiante['materias'])}")

# Agregar nueva información
estudiante["promedio"] = 8.5
print(f"Promedio: {estudiante['promedio']}")
`;
        }
        
        return example.trim() || '# Escribe tu código aquí...';
    }

    // Buscar ejemplos por concepto
    searchExamples(query) {
        const results = [];
        
        Object.keys(this.examples).forEach(type => {
            const info = this.getExampleInfo(type);
            const example = this.getExample(type);
            
            if (info && example) {
                const searchText = `${info.title} ${info.description} ${info.concepts.join(' ')} ${example}`.toLowerCase();
                
                if (searchText.includes(query.toLowerCase())) {
                    results.push({
                        type,
                        info,
                        relevance: this.calculateRelevance(query, searchText)
                    });
                }
            }
        });
        
        return results.sort((a, b) => b.relevance - a.relevance);
    }

    calculateRelevance(query, text) {
        const queryWords = query.toLowerCase().split(' ');
        let relevance = 0;
        
        queryWords.forEach(word => {
            const regex = new RegExp(word, 'gi');
            const matches = text.match(regex);
            if (matches) {
                relevance += matches.length;
            }
        });
        
        return relevance;
    }

    // Validar ejemplo antes de cargarlo
    validateExample(code) {
        // Validaciones básicas
        const issues = [];
        
        // Verificar que no esté vacío
        if (!code.trim()) {
            issues.push('El código está vacío');
        }
        
        // Verificar sintaxis básica de Python
        const lines = code.split('\n');
        let indentLevel = 0;
        
        lines.forEach((line, index) => {
            const trimmedLine = line.trim();
            if (!trimmedLine || trimmedLine.startsWith('#')) return;
            
            // Verificar indentación básica
            const currentIndent = line.length - line.trimStart().length;
            
            if (line.includes('\t') && line.includes('    ')) {
                issues.push(`Línea ${index + 1}: Mezcla de tabs y espacios`);
            }
            
            // Verificar paréntesis básicos
            const openParens = (line.match(/\(/g) || []).length;
            const closeParens = (line.match(/\)/g) || []).length;
            
            if (openParens !== closeParens && !line.trim().endsWith(':')) {
                issues.push(`Línea ${index + 1}: Paréntesis no balanceados`);
            }
        });
        
        return {
            valid: issues.length === 0,
            issues
        };
    }
}

// Inicializar gestor de ejemplos
document.addEventListener('DOMContentLoaded', () => {
    window.examplesManager = new ExamplesManager();
    
    // Configurar botones de ejemplo si existen
    const exampleButtons = document.querySelectorAll('.example-btn');
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const type = e.currentTarget.dataset.example;
            window.examplesManager.loadExample(type);
        });
    });
});
