from flask import Flask, render_template, request, jsonify
import os
from database import DatabaseManager
from evaluador import EvaluadorCodigo
from ejercicios import BibliotecaEjercicios

app = Flask(__name__)
#CORS(app)  # Permitir CORS para desarrollo

# Configuración
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/evaluador')
def evaluador():
    """Página del evaluador de código"""
    return render_template('evaluador.html')

@app.route('/api/evaluar', methods=['POST'])
def evaluar_codigo():
    """Endpoint para evaluar código Python"""
    try:
        data = request.get_json()
        
        if not data or 'codigo' not in data:
            return jsonify({
                'error': 'No se proporcionó código para evaluar',
                'feedback': [],
                'metricas': {},
                'score': 0
            }), 400
        
        codigo = data.get('codigo', '').strip()
        
        if not codigo:
            return jsonify({
                'error': 'El código está vacío',
                'feedback': [],
                'metricas': {},
                'score': 0
            }), 400
        
        # Crear evaluador y analizar código
        evaluador = EvaluadorCodigo()
        resultado = evaluador.evaluar_codigo_completo(codigo)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}',
            'feedback': [],
            'metricas': {},
            'score': 0
        }), 500

@app.route('/api/ejecutar', methods=['POST'])
def ejecutar_codigo():
    """Endpoint para ejecutar código Python de forma segura"""
    try:
        data = request.get_json()
        codigo = data.get('codigo', '').strip()
        
        if not codigo:
            return jsonify({
                'error': 'No hay código para ejecutar',
                'output': '',
                'success': False
            })
        
        # Crear evaluador y ejecutar código
        evaluador = EvaluadorCodigo()
        resultado = evaluador.ejecutar_codigo_seguro(codigo)
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({
            'error': f'Error al ejecutar código: {str(e)}',
            'output': '',
            'success': False
        })

@app.route('/api/ejemplos')
def obtener_ejemplos():
    """Endpoint para obtener ejemplos de código"""
    ejemplos = {
        'basic': '''def calcular_factorial(n):
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
    print(f"Error: {e}")''',

        'loop': '''# Análisis de datos con bucles y condicionales
import random

def analizar_ventas():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
    ventas = [random.randint(1000, 5000) for _ in range(len(meses))]
    total_ventas = sum(ventas)
    promedio = total_ventas / len(meses)
    print("📊 REPORTE DE VENTAS")
    for mes, venta in zip(meses, ventas):
        print(f"{mes}: ${venta:,}")
    print(f"Promedio mensual: ${promedio:,.2f}")

resultado = analizar_ventas()
print(f"✅ Análisis completado: {resultado}")''',

        'class': '''class GestorInventario:
    """Sistema de gestión de inventario para una tienda"""

    def __init__(self):
        self.productos = {}

    def agregar_producto(self, nombre, precio, stock=0):
        self.productos[nombre] = {"precio": precio, "stock": stock}
        print(f"Producto {nombre} agregado.")

    def mostrar_productos(self):
        for nombre, datos in self.productos.items():
            print(f"{nombre}: {datos['stock']} unidades a ${datos['precio']}")

# Demo
inventario = GestorInventario()
inventario.agregar_producto("Laptop", 800, 10)
inventario.agregar_producto("Mouse", 25, 50)
inventario.mostrar_productos()'''
    }

    return jsonify(ejemplos)

@app.route('/api/evaluar-ia', methods=['POST'])
def evaluar_con_inteligencia_artificial():
    """Endpoint que usa IA real para evaluación adaptativa"""
    try:
        data = request.get_json()
        codigo = data.get('codigo', '').strip()
        
        if not codigo:
            return jsonify({'error': 'Código vacío'}), 400
        
        evaluador = EvaluadorCodigo()
        resultado_ia = evaluador.evaluar_con_ia(codigo)
        
        return jsonify(resultado_ia)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estudiante/registrar', methods=['POST'])
def registrar_estudiante():
    """Registrar nuevo estudiante"""
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    
    if not nombre:
        return jsonify({'error': 'Nombre requerido'}), 400
    
    db = DatabaseManager()
    resultado = db.agregar_estudiante(nombre)
    
    return jsonify(resultado)

@app.route('/api/estudiante/<int:estudiante_id>/progreso', methods=['GET'])
def obtener_progreso_estudiante(estudiante_id):
    """Obtener progreso de un estudiante"""
    try:
        db = DatabaseManager()
        progreso = db.obtener_progreso(estudiante_id)
        
        if progreso:
            return jsonify(progreso)
        else:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
    except Exception as e:
        print(f"Error en progreso: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estudiantes', methods=['GET'])
def listar_todos_estudiantes():
    """Listar todos los estudiantes"""
    db = DatabaseManager()
    estudiantes = db.listar_estudiantes()
    return jsonify(estudiantes)

@app.route('/api/estadisticas', methods=['GET'])
def estadisticas_generales():
    """Estadísticas del sistema"""
    db = DatabaseManager()
    stats = db.obtener_estadisticas_generales()
    return jsonify(stats)

@app.route('/api/ejercicios/<nivel>', methods=['GET'])
def obtener_ejercicios(nivel):
    """Obtener ejercicios por nivel"""
    biblioteca = BibliotecaEjercicios()
    ejercicios = biblioteca.obtener_ejercicios_por_nivel(nivel)
    return jsonify(ejercicios)

@app.route('/api/ejercicio/<ejercicio_id>', methods=['GET'])
def obtener_ejercicio_especifico(ejercicio_id):
    """Obtener un ejercicio específico"""
    biblioteca = BibliotecaEjercicios()
    ejercicio = biblioteca.obtener_ejercicio(ejercicio_id)
    
    if ejercicio:
        return jsonify(ejercicio)
    return jsonify({'error': 'Ejercicio no encontrado'}), 404

@app.route('/api/ejercicio/aleatorio/<nivel>', methods=['GET'])
def ejercicio_aleatorio(nivel):
    """Obtener ejercicio aleatorio de un nivel"""
    biblioteca = BibliotecaEjercicios()
    ejercicio = biblioteca.obtener_ejercicio_aleatorio(nivel)
    
    if ejercicio:
        return jsonify(ejercicio)
    return jsonify({'error': 'No hay ejercicios para ese nivel'}), 404

@app.route('/api/estudiante/<int:estudiante_id>/badges', methods=['GET'])
def obtener_badges_estudiante(estudiante_id):
    """Obtener badges del estudiante"""
    db = DatabaseManager()
    badges = db.actualizar_badges(estudiante_id)
    return jsonify({'badges': badges})

@app.route('/api/badges/todos', methods=['GET'])
def listar_todos_badges():
    """Listar todos los badges disponibles"""
    from badges import SistemaBadges
    sistema = SistemaBadges()
    todos = sistema.obtener_todos_badges()
    return jsonify({'badges': todos})

@app.route('/dashboard')
def dashboard():
    """Dashboard del estudiante"""
    return render_template('dashboard.html')

@app.route('/ejercicios')
def ejercicios():
    """Página de ejercicios"""
    return render_template('ejercicios.html')

@app.route('/profesor')
def profesor():
    """Panel del profesor"""
    return render_template('profesor.html')

# Ejecutar aplicación
if __name__ == '__main__':
    print("🌐 Iniciando servidor web...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    

