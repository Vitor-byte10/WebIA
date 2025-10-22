import ast
import sys
import io
import contextlib
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

class AnalizadorAST(ast.NodeVisitor):
    """Analizador avanzado de AST de Python"""
    
    def __init__(self):
        self.metricas = {
            'funciones': [],
            'clases': [],
            'imports': [],
            'variables': [],
            'complejidad_ciclomatica': 1,
            'lineas_codigo': 0,
            'lineas_comentarios': 0,
            'lineas_vacias': 0
        }
        self.buenas_practicas = {
            'tiene_docstrings': False,
            'tiene_type_hints': False,
            'nombres_descriptivos': False,
            'manejo_errores': False,
            'usa_f_strings': False
        }
        
    def visit_FunctionDef(self, node):
        """Analiza definiciones de funciones"""
        funcion_info = {
            'nombre': node.name,
            'linea': node.lineno,
            'argumentos': len(node.args.args),
            'tiene_docstring': ast.get_docstring(node) is not None,
            'complejidad': 1
        }
        
        if node.returns or any(arg.annotation for arg in node.args.args):
            self.buenas_practicas['tiene_type_hints'] = True
        
        if funcion_info['tiene_docstring']:
            self.buenas_practicas['tiene_docstrings'] = True
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                funcion_info['complejidad'] += 1
                self.metricas['complejidad_ciclomatica'] += 1
        
        self.metricas['funciones'].append(funcion_info)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Analiza definiciones de clases"""
        clase_info = {
            'nombre': node.name,
            'linea': node.lineno,
            'metodos': 0,
            'tiene_docstring': ast.get_docstring(node) is not None
        }
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                clase_info['metodos'] += 1
        
        if clase_info['tiene_docstring']:
            self.buenas_practicas['tiene_docstrings'] = True
        
        self.metricas['clases'].append(clase_info)
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Analiza imports"""
        for alias in node.names:
            self.metricas['imports'].append({
                'tipo': 'import',
                'modulo': alias.name,
                'alias': alias.asname
            })
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Analiza imports from"""
        for alias in node.names:
            self.metricas['imports'].append({
                'tipo': 'from',
                'modulo': node.module,
                'nombre': alias.name,
                'alias': alias.asname
            })
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Analiza asignaciones de variables"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.metricas['variables'].append({
                    'nombre': target.id,
                    'linea': node.lineno
                })
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Detecta manejo de errores"""
        self.buenas_practicas['manejo_errores'] = True
        self.metricas['complejidad_ciclomatica'] += len(node.handlers)
        self.generic_visit(node)
    
    def visit_JoinedStr(self, node):
        """Detecta f-strings"""
        self.buenas_practicas['usa_f_strings'] = True
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Incrementa complejidad por condicionales"""
        self.metricas['complejidad_ciclomatica'] += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Incrementa complejidad por bucles while"""
        self.metricas['complejidad_ciclomatica'] += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Incrementa complejidad por bucles for"""
        self.metricas['complejidad_ciclomatica'] += 1
        self.generic_visit(node)

class EvaluadorCodigo:
    """Evaluador completo de código Python"""
    
    def __init__(self):
        self.analizador = None
    
    def analizar_codigo_estatico(self, codigo: str) -> Dict[str, Any]:
        """Analiza el código sin ejecutarlo"""
        try:
            lineas = codigo.split('\n')
            lineas_codigo = len([l for l in lineas if l.strip() and not l.strip().startswith('#')])
            lineas_comentarios = len([l for l in lineas if l.strip().startswith('#')])
            lineas_vacias = len([l for l in lineas if not l.strip()])
            
            tree = ast.parse(codigo)
            self.analizador = AnalizadorAST()
            self.analizador.visit(tree)
            
            self.analizador.metricas.update({
                'lineas_codigo': lineas_codigo,
                'lineas_comentarios': lineas_comentarios,
                'lineas_vacias': lineas_vacias,
                'lineas_totales': len(lineas)
            })
            
            variables = self.analizador.metricas['variables']
            nombres_descriptivos = sum(1 for var in variables 
                                     if len(var['nombre']) > 2 and 
                                     var['nombre'] not in ['i', 'j', 'k', 'x', 'y', 'z'])
            
            if nombres_descriptivos > 0:
                self.analizador.buenas_practicas['nombres_descriptivos'] = True
            
            return {
                'metricas': self.analizador.metricas,
                'buenas_practicas': self.analizador.buenas_practicas,
                'sintaxis_valida': True
            }
            
        except SyntaxError as e:
            return {
                'error_sintaxis': {
                    'mensaje': str(e),
                    'linea': e.lineno,
                    'columna': e.offset
                },
                'sintaxis_valida': False
            }
        except Exception as e:
            return {
                'error': f"Error inesperado: {str(e)}",
                'sintaxis_valida': False
            }
    
    def generar_feedback(self, analisis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Genera feedback detallado basado en el análisis"""
        feedback = []
        
        if not analisis.get('sintaxis_valida', False):
            if 'error_sintaxis' in analisis:
                error = analisis['error_sintaxis']
                feedback.append({
                    'tipo': 'error',
                    'mensaje': f"Error de sintaxis en línea {error['linea']}: {error['mensaje']}"
                })
            else:
                feedback.append({
                    'tipo': 'error',
                    'mensaje': f"Error en el código: {analisis.get('error', 'Error desconocido')}"
                })
            return feedback
        
        metricas = analisis['metricas']
        buenas_practicas = analisis['buenas_practicas']
        
        if len(metricas['funciones']) > 0:
            feedback.append({
                'tipo': 'success',
                'mensaje': f"Excelente: {len(metricas['funciones'])} función(es) definida(s)"
            })
        
        if len(metricas['clases']) > 0:
            feedback.append({
                'tipo': 'success',
                'mensaje': f"Programación orientada a objetos: {len(metricas['clases'])} clase(s)"
            })
        
        if buenas_practicas['tiene_docstrings']:
            feedback.append({
                'tipo': 'success',
                'mensaje': "Código bien documentado con docstrings"
            })
        
        return feedback
    
    def generar_sugerencias(self, analisis: Dict[str, Any]) -> List[str]:
        """Genera sugerencias específicas de mejora"""
        if not analisis.get('sintaxis_valida', False):
            return ["Corrige los errores de sintaxis antes de continuar"]
        
        sugerencias = []
        metricas = analisis['metricas']
        
        if len(metricas['funciones']) == 0 and metricas['lineas_codigo'] > 10:
            sugerencias.append("Divide tu código en funciones para mejor organización")
        
        return sugerencias[:6]
    
    def calcular_puntuacion(self, analisis: Dict[str, Any]) -> int:
        """Calcula la puntuación de calidad del código (0-100)"""
        if not analisis.get('sintaxis_valida', False):
            return 0
        
        score = 0
        metricas = analisis['metricas']
        buenas_practicas = analisis['buenas_practicas']
        
        if len(metricas['funciones']) > 0:
            score += 25
        if len(metricas['clases']) > 0:
            score += 25
        if buenas_practicas['tiene_docstrings']:
            score += 15
        
        return min(max(score, 0), 100)
    
    def ejecutar_codigo_seguro(self, codigo: str, timeout: int = 5) -> Dict[str, Any]:
        """Ejecuta código Python de forma segura"""
        try:
            try:
                compile(codigo, '<string>', 'exec')
            except SyntaxError as e:
                return {
                    'success': False,
                    'error': f'Error de sintaxis en línea {e.lineno}: {e.msg}',
                    'output': ''
                }
            
            captured_output = io.StringIO()
            restricted_builtins = {
                'print': print,
                'len': len,
                'range': range,
                'sum': sum,
                'min': min,
                'max': max,
            }
            
            with contextlib.redirect_stdout(captured_output):
                with contextlib.redirect_stderr(captured_output):
                    exec(codigo, {'__builtins__': restricted_builtins})
            
            output = captured_output.getvalue()
            
            return {
                'success': True,
                'output': output if output else 'Código ejecutado sin salida visible',
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'{type(e).__name__}: {str(e)}',
                'output': ''
            }
    
    def evaluar_codigo_completo(self, codigo: str) -> Dict[str, Any]:
        """Evaluación completa del código con todas las métricas"""
        analisis = self.analizar_codigo_estatico(codigo)
        feedback = self.generar_feedback(analisis)
        sugerencias = self.generar_sugerencias(analisis)
        score = self.calcular_puntuacion(analisis)
        
        if analisis.get('sintaxis_valida', False):
            metricas_frontend = {
                'lineas_codigo': analisis['metricas']['lineas_codigo'],
                'funciones': len(analisis['metricas']['funciones']),
                'clases': len(analisis['metricas']['clases']),
                'complejidad': analisis['metricas']['complejidad_ciclomatica'],
            }
        else:
            metricas_frontend = {
                'lineas_codigo': 0,
                'funciones': 0,
                'clases': 0,
                'complejidad': 0,
            }
        
        return {
            'feedback': feedback,
            'sugerencias': sugerencias,
            'metricas': metricas_frontend,
            'score': score,
            'timestamp': datetime.now().isoformat()
        }
    
    def evaluar_con_ia(self, codigo):
        """Nueva función que usa IA real para evaluación adaptativa"""
        try:
            from ia_evaluador import EvaluadorInteligente
            evaluador_ia = EvaluadorInteligente()
            return evaluador_ia.evaluacion_completa_con_ia(codigo)
        except ImportError:
            return {'error': 'Módulo de IA no disponible'}
    
    def evaluar_y_guardar(self, codigo, estudiante_id=None):
        """Evaluar código y guardar en base de datos"""
        resultado = self.evaluar_codigo_completo(codigo)
        
        if estudiante_id:
            try:
                from database import DatabaseManager
                db = DatabaseManager()
                resultado['codigo'] = codigo
                db.guardar_evaluacion(estudiante_id, resultado)
            except ImportError:
                pass
        
        return resultado
