import re
import math
from collections import Counter
from typing import Dict, List, Tuple, Any

class ClasificadorNivel:
    """Clasificador de IA que determina automáticamente el nivel del programador"""
    
    def __init__(self):
        # Patrones que indican diferentes niveles de habilidad
        self.patrones_principiante = {
            'variables_simples': r'\b[a-z]+\s*=\s*[0-9]+',
            'print_basico': r'print\([^)]*\)',
            'input_basico': r'input\([^)]*\)',
            'operaciones_basicas': r'[+\-*/]\s*',
            'if_simple': r'if\s+\w+\s*[<>=!]+',
        }
        
        self.patrones_intermedio = {
            'funciones_con_parametros': r'def\s+\w+\([^)]+\):',
            'listas_comprension': r'\[.*for.*in.*\]',
            'manejo_errores': r'try:|except:',
            'imports': r'import\s+\w+|from\s+\w+\s+import',
            'diccionarios': r'\{.*:.*\}',
            'bucles_while': r'while\s+.*:',
            'f_strings': r'f["\'][^"\']*\{.*\}[^"\']*["\']',
        }
        
        self.patrones_avanzado = {
            'clases': r'class\s+\w+.*:',
            'decoradores': r'@\w+',
            'generadores': r'yield\s+',
            'context_managers': r'with\s+.*as\s+.*:',
            'lambda': r'lambda\s+.*:',
            'herencia': r'class\s+\w+\([^)]+\):',
            'metaclases': r'__\w+__',
            'type_hints': r':\s*\w+\s*=|def\s+\w+\([^)]*:\s*\w+\)',
        }
        
        # Pesos para cada categoría
        self.pesos = {
            'principiante': 1.0,
            'intermedio': 2.0,
            'avanzado': 3.5
        }

    def analizar_complejidad_sintactica(self, codigo: str) -> Dict[str, float]:
        """Analiza la complejidad sintáctica del código"""
        puntuaciones = {'principiante': 0, 'intermedio': 0, 'avanzado': 0}
        
        # Contar patrones de cada nivel
        for nivel, patrones in [
            ('principiante', self.patrones_principiante),
            ('intermedio', self.patrones_intermedio),
            ('avanzado', self.patrones_avanzado)
        ]:
            for nombre_patron, patron in patrones.items():
                matches = len(re.findall(patron, codigo, re.MULTILINE))
                puntuaciones[nivel] += matches * self.pesos[nivel]
        
        return puntuaciones

    def analizar_estructura_codigo(self, codigo: str) -> Dict[str, float]:
        """Analiza la estructura y organización del código"""
        lineas = codigo.split('\n')
        lineas_codigo = [l for l in lineas if l.strip() and not l.strip().startswith('#')]
        
        if not lineas_codigo:
            return {'principiante': 1, 'intermedio': 0, 'avanzado': 0}
        
        # Métricas de estructura
        total_lineas = len(lineas_codigo)
        funciones = len(re.findall(r'def\s+\w+', codigo))
        clases = len(re.findall(r'class\s+\w+', codigo))
        comentarios = len([l for l in lineas if l.strip().startswith('#')])
        docstrings = len(re.findall(r'""".*?"""', codigo, re.DOTALL))
        
        # Calcular ratios
        ratio_funciones = funciones / max(total_lineas / 10, 1)
        ratio_comentarios = comentarios / max(total_lineas, 1)
        ratio_documentacion = docstrings / max(funciones, 1)
        
        # Puntuación basada en estructura
        puntuacion_estructura = {
            'principiante': 0,
            'intermedio': 0,
            'avanzado': 0
        }
        
        # Lógica de puntuación estructural
        if total_lineas <= 20 and funciones <= 1:
            puntuacion_estructura['principiante'] += 5
        elif total_lineas <= 50 and funciones <= 3:
            puntuacion_estructura['intermedio'] += 5
        else:
            puntuacion_estructura['avanzado'] += 5
            
        if clases > 0:
            puntuacion_estructura['avanzado'] += 10
            
        if ratio_comentarios > 0.1:
            puntuacion_estructura['intermedio'] += 3
            
        if ratio_documentacion > 0.5:
            puntuacion_estructura['avanzado'] += 5
        
        return puntuacion_estructura

    def clasificar_nivel(self, codigo: str) -> Dict[str, Any]:
        """Clasificador principal que determina el nivel del programador"""
        
        # Análisis sintáctico
        puntuacion_sintaxis = self.analizar_complejidad_sintactica(codigo)
        
        # Análisis estructural
        puntuacion_estructura = self.analizar_estructura_codigo(codigo)
        
        # Combinar puntuaciones con pesos
        puntuacion_total = {
            'principiante': puntuacion_sintaxis['principiante'] * 0.7 + puntuacion_estructura['principiante'] * 0.3,
            'intermedio': puntuacion_sintaxis['intermedio'] * 0.6 + puntuacion_estructura['intermedio'] * 0.4,
            'avanzado': puntuacion_sintaxis['avanzado'] * 0.5 + puntuacion_estructura['avanzado'] * 0.5
        }
        
        # Normalizar puntuaciones
        total_puntos = sum(puntuacion_total.values())
        if total_puntos > 0:
            probabilidades = {k: v/total_puntos for k, v in puntuacion_total.items()}
        else:
            probabilidades = {'principiante': 1.0, 'intermedio': 0.0, 'avanzado': 0.0}
        
        # Determinar nivel más probable
        nivel_predicho = max(probabilidades, key=probabilidades.get)
        confianza = probabilidades[nivel_predicho]
        
        return {
            'nivel_predicho': nivel_predicho,
            'confianza': round(confianza * 100, 1),
            'probabilidades': {k: round(v*100, 1) for k, v in probabilidades.items()},
            'puntuaciones_raw': puntuacion_total,
            'detalles': {
                'sintaxis': puntuacion_sintaxis,
                'estructura': puntuacion_estructura
            }
        }


class SistemaRecomendacionesAdaptativo:
    """Sistema de IA que genera recomendaciones personalizadas"""
    
    def __init__(self):
        self.recomendaciones_por_nivel = {
            'principiante': {
                'ejercicios': [
                    "Práctica con variables y tipos de datos básicos",
                    "Ejercicios de entrada y salida (input/print)",
                    "Estructuras condicionales simples (if/else)",
                    "Bucles básicos (for con range)"
                ],
                'conceptos': [
                    "Sintaxis básica de Python",
                    "Operadores aritméticos y de comparación", 
                    "Tipos de datos (int, str, float, bool)",
                    "Estructuras de control básicas"
                ]
            },
            'intermedio': {
                'ejercicios': [
                    "Crear funciones con múltiples parámetros",
                    "Trabajar con listas y diccionarios",
                    "Implementar manejo de errores",
                    "Usar list comprehensions"
                ],
                'conceptos': [
                    "Funciones y scope de variables",
                    "Estructuras de datos complejas",
                    "Manejo de excepciones",
                    "Módulos e imports"
                ]
            },
            'avanzado': {
                'ejercicios': [
                    "Diseñar clases con herencia",
                    "Implementar patrones de diseño",
                    "Usar decoradores y context managers",
                    "Optimización y profiling de código"
                ],
                'conceptos': [
                    "Programación orientada a objetos avanzada",
                    "Metaclases y descriptores",
                    "Programación funcional",
                    "Concurrencia y paralelismo"
                ]
            }
        }
        
        self.patrones_error_comunes = {
            'indentacion_incorrecta': r'^[^\s].*:\n[^\s]',
            'variables_no_definidas': r'\b[a-z_][a-zA-Z0-9_]*\b(?=\s*[^=])',
            'parentesis_desbalanceados': r'\([^)]*$|^[^(]*\)',
            'sintaxis_print_python2': r'print\s+[^(]',
        }

    def analizar_errores_comunes(self, codigo: str) -> List[str]:
        """Detecta patrones de errores comunes"""
        errores_detectados = []
        
        for error, patron in self.patrones_error_comunes.items():
            if re.search(patron, codigo, re.MULTILINE):
                errores_detectados.append(error)
        
        return errores_detectados

    def generar_recomendaciones(self, nivel: str, codigo: str, errores: List[str]) -> Dict[str, List[str]]:
        """Genera recomendaciones adaptativas basadas en el nivel y errores"""
        
        recomendaciones_base = self.recomendaciones_por_nivel.get(nivel, self.recomendaciones_por_nivel['principiante'])
        
        # Recomendaciones específicas por errores detectados
        recomendaciones_errores = []
        
        if 'indentacion_incorrecta' in errores:
            recomendaciones_errores.append("Revisa la indentación: usa 4 espacios consistentemente")
            
        if 'sintaxis_print_python2' in errores:
            recomendaciones_errores.append("Usa print() con paréntesis en Python 3")
            
        # Recomendaciones adaptativas según características del código
        recomendaciones_adaptativas = []
        
        if nivel == 'principiante' and 'def' in codigo:
            recomendaciones_adaptativas.append("¡Buen trabajo usando funciones! Intenta agregar docstrings")
            
        if nivel == 'intermedio' and 'class' not in codigo and len(codigo.split('\n')) > 30:
            recomendaciones_adaptativas.append("Considera organizar tu código en clases")
            
        if 'try' not in codigo and 'except' not in codigo:
            recomendaciones_adaptativas.append("Considera agregar manejo de errores con try/except")
        
        return {
            'ejercicios_sugeridos': recomendaciones_base['ejercicios'],
            'conceptos_estudiar': recomendaciones_base['conceptos'],
            'correcciones_inmediatas': recomendaciones_errores,
            'siguiente_nivel': recomendaciones_adaptativas
        }


class PredictorDificultad:
    """Algoritmo de IA que predice la dificultad de un ejercicio para el estudiante"""
    
    def __init__(self):
        self.metricas_dificultad = {
            'complejidad_ciclomatica': 0.3,
            'profundidad_anidamiento': 0.2,
            'numero_conceptos': 0.25,
            'longitud_codigo': 0.15,
            'nivel_abstraccion': 0.1
        }

    def calcular_complejidad_ciclomatica(self, codigo: str) -> int:
        """Calcula la complejidad ciclomática del código"""
        # Contar puntos de decisión
        puntos_decision = len(re.findall(r'\b(if|elif|while|for|except|and|or)\b', codigo))
        return puntos_decision + 1

    def calcular_profundidad_anidamiento(self, codigo: str) -> int:
        """Calcula la profundidad máxima de anidamiento"""
        lineas = codigo.split('\n')
        max_profundidad = 0
        profundidad_actual = 0
        
        for linea in lineas:
            if linea.strip():
                # Contar espacios de indentación
                espacios = len(linea) - len(linea.lstrip())
                profundidad_actual = espacios // 4
                max_profundidad = max(max_profundidad, profundidad_actual)
        
        return max_profundidad

    def contar_conceptos_unicos(self, codigo: str) -> int:
        """Cuenta conceptos únicos de programación en el código"""
        conceptos = set()
        
        # Patrones de conceptos
        patrones_conceptos = {
            'variables': r'\b\w+\s*=',
            'funciones': r'def\s+\w+',
            'clases': r'class\s+\w+',
            'bucles_for': r'for\s+',
            'bucles_while': r'while\s+',
            'condicionales': r'if\s+',
            'listas': r'\[.*\]',
            'diccionarios': r'\{.*:.*\}',
            'imports': r'import\s+',
            'excepciones': r'try:|except:',
        }
        
        for concepto, patron in patrones_conceptos.items():
            if re.search(patron, codigo):
                conceptos.add(concepto)
        
        return len(conceptos)

    def predecir_dificultad(self, codigo: str, nivel_estudiante: str) -> Dict[str, Any]:
        """Predice la dificultad del código para el estudiante"""
        
        # Calcular métricas
        complejidad = self.calcular_complejidad_ciclomatica(codigo)
        profundidad = self.calcular_profundidad_anidamiento(codigo)
        conceptos = self.contar_conceptos_unicos(codigo)
        longitud = len(codigo.split('\n'))
        
        # Nivel de abstracción (heurística)
        nivel_abstraccion = 0
        if 'class' in codigo: nivel_abstraccion += 2
        if 'lambda' in codigo: nivel_abstraccion += 2
        if '@' in codigo: nivel_abstraccion += 1  # decoradores
        if 'yield' in codigo: nivel_abstraccion += 2  # generadores
        
        # Normalizar métricas (escala 0-10)
        metricas_normalizadas = {
            'complejidad_ciclomatica': min(complejidad / 5, 10),
            'profundidad_anidamiento': min(profundidad * 2, 10),
            'numero_conceptos': min(conceptos / 2, 10),
            'longitud_codigo': min(longitud / 20, 10),
            'nivel_abstraccion': min(nivel_abstraccion, 10)
        }
        
        # Calcular dificultad ponderada
        dificultad_base = sum(
            metrica * peso 
            for metrica, peso in zip(metricas_normalizadas.values(), self.metricas_dificultad.values())
        )
        
        # Ajustar según nivel del estudiante
        ajustes_nivel = {
            'principiante': 1.2,  # Más difícil para principiantes
            'intermedio': 1.0,    # Neutral
            'avanzado': 0.8       # Más fácil para avanzados
        }
        
        dificultad_ajustada = dificultad_base * ajustes_nivel.get(nivel_estudiante, 1.0)
        
        # Clasificar dificultad
        if dificultad_ajustada <= 3:
            categoria = 'Fácil'
        elif dificultad_ajustada <= 6:
            categoria = 'Moderado'
        elif dificultad_ajustada <= 8:
            categoria = 'Difícil'
        else:
            categoria = 'Muy Difícil'
        
        return {
            'dificultad_numerica': round(dificultad_ajustada, 2),
            'categoria_dificultad': categoria,
            'metricas_detalladas': metricas_normalizadas,
            'recomendacion_tiempo': self.estimar_tiempo_resolucion(dificultad_ajustada),
            'sugerencias_ayuda': self.generar_sugerencias_ayuda(categoria, nivel_estudiante)
        }

    def estimar_tiempo_resolucion(self, dificultad: float) -> str:
        """Estima tiempo necesario para resolver el ejercicio"""
        minutos = int(dificultad * 15)  # 15 minutos por punto de dificultad
        
        if minutos <= 30:
            return f"~{minutos} minutos"
        elif minutos <= 120:
            horas = minutos // 60
            return f"~{horas} hora(s)"
        else:
            return "Varias sesiones"

    def generar_sugerencias_ayuda(self, categoria: str, nivel: str) -> List[str]:
        """Genera sugerencias de ayuda adaptativas"""
        
        sugerencias_base = {
            'Fácil': [
                "Perfecto para practicar conceptos básicos",
                "Intenta resolverlo sin ayuda primero"
            ],
            'Moderado': [
                "Tómate tu tiempo para planificar la solución",
                "Divide el problema en pasos más pequeños"
            ],
            'Difícil': [
                "Considera buscar ejemplos similares primero",
                "No dudes en pedir ayuda si te atascas"
            ],
            'Muy Difícil': [
                "Problema avanzado - requiere conocimientos sólidos",
                "Recomendado trabajar en equipo o con mentor"
            ]
        }
        
        return sugerencias_base.get(categoria, [])


class EvaluadorInteligente:
    """Clase principal que integra todos los componentes de IA"""
    
    def __init__(self):
        self.clasificador = ClasificadorNivel()
        self.recomendador = SistemaRecomendacionesAdaptativo()
        self.predictor = PredictorDificultad()
        
    def evaluacion_completa_con_ia(self, codigo: str) -> Dict[str, Any]:
        """Evaluación completa usando todos los componentes de IA"""
        
        # 1. Clasificar nivel del estudiante
        clasificacion = self.clasificador.clasificar_nivel(codigo)
        nivel_estudiante = clasificacion['nivel_predicho']
        
        # 2. Detectar errores comunes
        errores = self.recomendador.analizar_errores_comunes(codigo)
        
        # 3. Generar recomendaciones adaptativas
        recomendaciones = self.recomendador.generar_recomendaciones(
            nivel_estudiante, codigo, errores
        )
        
        # 4. Predecir dificultad del ejercicio
        prediccion_dificultad = self.predictor.predecir_dificultad(codigo, nivel_estudiante)
        
        # 5. Compilar resultado final
        return {
            'clasificacion_nivel': clasificacion,
            'errores_detectados': errores,
            'recomendaciones_adaptativas': recomendaciones,
            'analisis_dificultad': prediccion_dificultad,
            'timestamp': self._obtener_timestamp()
        }
    
    def _obtener_timestamp(self):
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
