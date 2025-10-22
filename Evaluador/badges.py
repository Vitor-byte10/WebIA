class SistemaBadges:
    def __init__(self):
        self.badges = {
            'primer_codigo': {
                'nombre': 'Primer Código',
                'descripcion': 'Evaluaste tu primer código',
                'icono': '🎯',
                'criterio': lambda datos: datos['evaluaciones_totales'] >= 1
            },
            'perfeccionista': {
                'nombre': 'Perfeccionista',
                'descripcion': 'Obtuviste un score de 100%',
                'icono': '⭐',
                'criterio': lambda datos: datos['score_maximo'] == 100
            },
            'persistente': {
                'nombre': 'Persistente',
                'descripcion': 'Completaste 10 evaluaciones',
                'icono': '💪',
                'criterio': lambda datos: datos['evaluaciones_totales'] >= 10
            },
            'maestro_funciones': {
                'nombre': 'Maestro de Funciones',
                'descripcion': 'Creaste 5 funciones correctamente',
                'icono': '⚙️',
                'criterio': lambda datos: datos['funciones_creadas'] >= 5
            },
            'oop_expert': {
                'nombre': 'Experto en OOP',
                'descripcion': 'Implementaste 3 clases diferentes',
                'icono': '🏗️',
                'criterio': lambda datos: datos['clases_creadas'] >= 3
            },
            'nivel_intermedio': {
                'nombre': 'Nivel Intermedio',
                'descripcion': 'Alcanzaste nivel intermedio',
                'icono': '📈',
                'criterio': lambda datos: datos['nivel_actual'] == 'intermedio'
            },
            'nivel_avanzado': {
                'nombre': 'Nivel Avanzado',
                'descripcion': 'Alcanzaste nivel avanzado',
                'icono': '🚀',
                'criterio': lambda datos: datos['nivel_actual'] == 'avanzado'
            },
            'dedicado': {
                'nombre': 'Dedicado',
                'descripcion': 'Completaste 20 evaluaciones',
                'icono': '🔥',
                'criterio': lambda datos: datos['evaluaciones_totales'] >= 20
            },
            'aprobado': {
                'nombre': 'Aprobado',
                'descripcion': 'Obtuviste promedio mayor a 70',
                'icono': '✅',
                'criterio': lambda datos: datos.get('score_promedio', 0) >= 70
            }
        }
    
    def verificar_badges(self, datos_estudiante):
        """Verifica qué badges ha obtenido el estudiante"""
        badges_obtenidos = []
        
        for badge_id, badge_info in self.badges.items():
            try:
                if badge_info['criterio'](datos_estudiante):
                    badges_obtenidos.append({
                        'id': badge_id,
                        'nombre': badge_info['nombre'],
                        'descripcion': badge_info['descripcion'],
                        'icono': badge_info['icono']
                    })
            except KeyError:
                continue
        
        return badges_obtenidos
    
    def obtener_todos_badges(self):
        """Retorna todos los badges disponibles"""
        return [
            {
                'id': badge_id,
                'nombre': info['nombre'],
                'descripcion': info['descripcion'],
                'icono': info['icono']
            }
            for badge_id, info in self.badges.items()
        ]
    
    def verificar_nuevo_badge(self, badges_anteriores, badges_actuales):
        """Compara badges y retorna los nuevos obtenidos"""
        ids_anteriores = set(badges_anteriores)
        ids_actuales = set([b['id'] for b in badges_actuales])
        
        nuevos_ids = ids_actuales - ids_anteriores
        
        return [b for b in badges_actuales if b['id'] in nuevos_ids]
