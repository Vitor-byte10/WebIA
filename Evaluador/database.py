import sqlite3
from datetime import datetime
import json
import os

class DatabaseManager:
    def __init__(self, db_path='./estudiantes.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Crear tablas si no existen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de estudiantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                nivel_inicial TEXT DEFAULT 'principiante',
                fecha_registro TEXT NOT NULL
            )
        ''')
        
        # Tabla de evaluaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER NOT NULL,
                codigo_evaluado TEXT,
                nivel_detectado TEXT,
                score INTEGER,
                complejidad INTEGER,
                funciones INTEGER,
                clases INTEGER,
                fecha TEXT NOT NULL,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
            )
        ''')
        
        # Tabla de progreso
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progreso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER UNIQUE NOT NULL,
                ejercicios_completados INTEGER DEFAULT 0,
                evaluaciones_totales INTEGER DEFAULT 0,
                funciones_creadas INTEGER DEFAULT 0,
                clases_creadas INTEGER DEFAULT 0,
                score_maximo INTEGER DEFAULT 0,
                score_promedio REAL DEFAULT 0,
                badges_obtenidos TEXT DEFAULT '[]',
                nivel_actual TEXT DEFAULT 'principiante',
                ultima_actividad TEXT,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
            )
        ''')
        
        # Tabla de sesiones activas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                activa INTEGER DEFAULT 1,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente")
    
    def agregar_estudiante(self, nombre):
        """Registrar nuevo estudiante"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute('SELECT id FROM estudiantes WHERE nombre = ?', (nombre,))
            existe = cursor.fetchone()
            
            if existe:
                conn.close()
                return {'error': 'El estudiante ya existe', 'estudiante_id': existe[0]}
            
            # Insertar estudiante
            cursor.execute('''
                INSERT INTO estudiantes (nombre, fecha_registro)
                VALUES (?, ?)
            ''', (nombre, datetime.now().isoformat()))
            estudiante_id = cursor.lastrowid
            
            # Crear registro de progreso inicial
            cursor.execute('''
                INSERT INTO progreso (estudiante_id, nivel_actual, ultima_actividad)
                VALUES (?, 'principiante', ?)
            ''', (estudiante_id, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return {'estudiante_id': estudiante_id, 'nombre': nombre}
        
        except Exception as e:
            return {'error': str(e)}
    
    def iniciar_sesion(self, estudiante_id):
        """Iniciar sesión de estudiante"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sesiones (estudiante_id, fecha_inicio)
            VALUES (?, ?)
        ''', (estudiante_id, datetime.now().isoformat()))
        sesion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return sesion_id
    
    def guardar_evaluacion(self, estudiante_id, resultado_evaluacion):
        """Guardar resultado de evaluación"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extraer datos del resultado
            codigo = resultado_evaluacion.get('codigo', '')
            nivel = resultado_evaluacion.get('clasificacion_nivel', {}).get('nivel_predicho', 'principiante')
            score = resultado_evaluacion.get('score', 0)
            metricas = resultado_evaluacion.get('metricas', {})
            
            # Guardar evaluación
            cursor.execute('''
                INSERT INTO evaluaciones (
                    estudiante_id, codigo_evaluado, nivel_detectado, 
                    score, complejidad, funciones, clases, fecha
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                estudiante_id,
                codigo[:500],  # Limitar tamaño del código guardado
                nivel,
                score,
                metricas.get('complejidad', 0),
                metricas.get('funciones', 0),
                metricas.get('clases', 0),
                datetime.now().isoformat()
            ))
            
            # Actualizar progreso
            self._actualizar_progreso(cursor, estudiante_id, resultado_evaluacion)
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error guardando evaluación: {e}")
            return False
    
    def _actualizar_progreso(self, cursor, estudiante_id, resultado):
        """Actualizar el progreso del estudiante"""
        # Obtener progreso actual
        cursor.execute('SELECT * FROM progreso WHERE estudiante_id = ?', (estudiante_id,))
        progreso_actual = cursor.fetchone()
        
        if not progreso_actual:
            return
        
        # Extraer valores actuales
        eval_totales = progreso_actual[2] + 1
        funciones = progreso_actual[3] + resultado.get('metricas', {}).get('funciones', 0)
        clases = progreso_actual[4] + resultado.get('metricas', {}).get('clases', 0)
        score_nuevo = resultado.get('score', 0)
        score_max_actual = progreso_actual[5]
        score_promedio_actual = progreso_actual[6]
        
        # Calcular nuevo promedio
        score_maximo = max(score_max_actual, score_nuevo)
        score_promedio = ((score_promedio_actual * (eval_totales - 1)) + score_nuevo) / eval_totales
        
        # Determinar nivel actual basado en historial
        nivel_actual = resultado.get('clasificacion_nivel', {}).get('nivel_predicho', 'principiante')
        
        # Actualizar
        cursor.execute('''
            UPDATE progreso SET
                evaluaciones_totales = ?,
                funciones_creadas = ?,
                clases_creadas = ?,
                score_maximo = ?,
                score_promedio = ?,
                nivel_actual = ?,
                ultima_actividad = ?
            WHERE estudiante_id = ?
        ''', (
            eval_totales,
            funciones,
            clases,
            score_maximo,
            round(score_promedio, 2),
            nivel_actual,
            datetime.now().isoformat(),
            estudiante_id
        ))
    
    def obtener_estudiante_por_nombre(self, nombre):
        """Buscar estudiante por nombre"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM estudiantes WHERE nombre = ?', (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return {
                'id': resultado[0],
                'nombre': resultado[1],
                'nivel_inicial': resultado[2],
                'fecha_registro': resultado[3]
            }
        return None
    
    def obtener_progreso(self, estudiante_id):
        """Obtener progreso completo del estudiante"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Datos del estudiante
        cursor.execute('SELECT * FROM estudiantes WHERE id = ?', (estudiante_id,))
        estudiante = cursor.fetchone()
        
        # Progreso
        cursor.execute('SELECT * FROM progreso WHERE estudiante_id = ?', (estudiante_id,))
        progreso = cursor.fetchone()
        
        # Últimas evaluaciones
        cursor.execute('''
            SELECT score, nivel_detectado, fecha 
            FROM evaluaciones 
            WHERE estudiante_id = ? 
            ORDER BY fecha DESC 
            LIMIT 10
        ''', (estudiante_id,))
        evaluaciones = cursor.fetchall()
        
        conn.close()
        
        if not estudiante or not progreso:
            return None
        
        return {
            'estudiante': {
                'id': estudiante[0],
                'nombre': estudiante[1],
                'nivel_inicial': estudiante[2],
                'fecha_registro': estudiante[3]
            },
            'progreso': {
                'evaluaciones_totales': progreso[2],
                'funciones_creadas': progreso[3],
                'clases_creadas': progreso[4],
                'score_maximo': progreso[5],
                'score_promedio': progreso[6],
                'badges': json.loads(progreso[7]),
                'nivel_actual': progreso[8],
                'ultima_actividad': progreso[9]
            },
            'historial_reciente': [
                {
                    'score': ev[0],
                    'nivel': ev[1],
                    'fecha': ev[2]
                } for ev in evaluaciones
            ]
        }
    
    def listar_estudiantes(self):
        """Listar todos los estudiantes con su progreso"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.nombre, p.nivel_actual, p.evaluaciones_totales, 
                   p.score_promedio, p.ultima_actividad
            FROM estudiantes e
            LEFT JOIN progreso p ON e.id = p.estudiante_id
            ORDER BY p.ultima_actividad DESC
        ''')
        
        estudiantes = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': est[0],
                'nombre': est[1],
                'nivel': est[2] or 'principiante',
                'evaluaciones': est[3] or 0,
                'promedio': est[4] or 0,
                'ultima_actividad': est[5]
            } for est in estudiantes
        ]
    
    def obtener_estadisticas_generales(self):
        """Estadísticas del sistema completo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total estudiantes
        cursor.execute('SELECT COUNT(*) FROM estudiantes')
        total_estudiantes = cursor.fetchone()[0]
        
        # Total evaluaciones
        cursor.execute('SELECT COUNT(*) FROM evaluaciones')
        total_evaluaciones = cursor.fetchone()[0]
        
        # Promedio general
        cursor.execute('SELECT AVG(score_promedio) FROM progreso')
        promedio_general = cursor.fetchone()[0] or 0
        
        # Distribución por nivel
        cursor.execute('''
            SELECT nivel_actual, COUNT(*) 
            FROM progreso 
            GROUP BY nivel_actual
        ''')
        distribucion = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_estudiantes': total_estudiantes,
            'total_evaluaciones': total_evaluaciones,
            'promedio_general': round(promedio_general, 2),
            'distribucion_niveles': distribucion
        }

def actualizar_badges(self, estudiante_id):
    """Actualizar badges del estudiante"""
    from badges import SistemaBadges
    
    # Obtener datos del estudiante
    progreso = self.obtener_progreso(estudiante_id)
    if not progreso:
        return []
    
    # Preparar datos para verificación
    datos = {
        'evaluaciones_totales': progreso['progreso']['evaluaciones_totales'],
        'funciones_creadas': progreso['progreso']['funciones_creadas'],
        'clases_creadas': progreso['progreso']['clases_creadas'],
        'score_maximo': progreso['progreso']['score_maximo'],
        'nivel_actual': progreso['progreso']['nivel_actual']
    }
    
    # Verificar badges
    sistema_badges = SistemaBadges()
    badges_obtenidos = sistema_badges.verificar_badges(datos)
    
    # Guardar en BD
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE progreso SET badges_obtenidos = ?
        WHERE estudiante_id = ?
    ''', (json.dumps([b['id'] for b in badges_obtenidos]), estudiante_id))
    conn.commit()
    conn.close()
    
    return badges_obtenidos
