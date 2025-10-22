class BibliotecaEjercicios:
    def __init__(self):
        self.ejercicios = {
            'principiante': [
                {
                    'id': 'p1',
                    'titulo': 'Suma de dos números',
                    'descripcion': 'Crea una función llamada "sumar" que reciba dos números y retorne su suma',
                    'dificultad': 1,
                    'puntos': 10,
                    'codigo_plantilla': '''def sumar(a, b):
    # Escribe tu código aquí
    pass

# Prueba tu función
resultado = sumar(5, 3)
print(f"La suma es: {resultado}")''',
                    'pistas': [
                        'Usa el operador + para sumar',
                        'No olvides usar return para devolver el resultado',
                        'Los parámetros a y b son los números a sumar'
                    ],
                    'tests': [
                        {'input': (2, 3), 'output': 5, 'descripcion': 'sumar(2, 3) debe retornar 5'},
                        {'input': (10, 5), 'output': 15, 'descripcion': 'sumar(10, 5) debe retornar 15'},
                        {'input': (0, 0), 'output': 0, 'descripcion': 'sumar(0, 0) debe retornar 0'}
                    ]
                },
                {
                    'id': 'p2',
                    'titulo': 'Número par o impar',
                    'descripcion': 'Crea una función "es_par" que determine si un número es par',
                    'dificultad': 1,
                    'puntos': 10,
                    'codigo_plantilla': '''def es_par(numero):
    # Escribe tu código aquí
    pass

# Prueba tu función
print(es_par(4))  # Debe imprimir True
print(es_par(7))  # Debe imprimir False''',
                    'pistas': [
                        'Usa el operador módulo % para obtener el resto',
                        'Un número es par si el resto de dividirlo entre 2 es 0',
                        'Retorna True o False según corresponda'
                    ],
                    'tests': [
                        {'input': 4, 'output': True},
                        {'input': 7, 'output': False},
                        {'input': 0, 'output': True}
                    ]
                },
                {
                    'id': 'p3',
                    'titulo': 'Saludo personalizado',
                    'descripcion': 'Crea una función que salude a una persona por su nombre',
                    'dificultad': 1,
                    'puntos': 10,
                    'codigo_plantilla': '''def saludar(nombre):
    # Escribe tu código aquí
    pass

# Prueba tu función
saludar("Juan")  # Debe imprimir: Hola, Juan!''',
                    'pistas': [
                        'Usa print() para mostrar el mensaje',
                        'Usa f-strings para incluir el nombre: f"Hola, {nombre}!"',
                        'No necesitas return, solo print'
                    ],
                    'tests': []
                },
                {
                    'id': 'p4',
                    'titulo': 'Mayor de dos números',
                    'descripcion': 'Crea una función que retorne el mayor de dos números',
                    'dificultad': 2,
                    'puntos': 15,
                    'codigo_plantilla': '''def mayor(a, b):
    # Escribe tu código aquí
    pass

# Prueba
print(mayor(10, 5))  # Debe imprimir 10
print(mayor(3, 8))   # Debe imprimir 8''',
                    'pistas': [
                        'Usa una estructura if-else',
                        'Compara los números con el operador >',
                        'Retorna el número mayor'
                    ],
                    'tests': [
                        {'input': (10, 5), 'output': 10},
                        {'input': (3, 8), 'output': 8},
                        {'input': (5, 5), 'output': 5}
                    ]
                }
            ],
            'intermedio': [
                {
                    'id': 'i1',
                    'titulo': 'Contar vocales',
                    'descripcion': 'Crea una función que cuente cuántas vocales hay en un texto',
                    'dificultad': 3,
                    'puntos': 20,
                    'codigo_plantilla': '''def contar_vocales(texto):
    # Escribe tu código aquí
    pass

# Prueba
frase = "Hola Mundo"
cantidad = contar_vocales(frase)
print(f"Hay {cantidad} vocales")''',
                    'pistas': [
                        'Define una lista o string con las vocales: "aeiouAEIOU"',
                        'Recorre cada letra del texto con un bucle for',
                        'Usa un contador que incremente cuando encuentres una vocal'
                    ],
                    'tests': [
                        {'input': 'Hola', 'output': 2},
                        {'input': 'Python', 'output': 1},
                        {'input': 'Programacion', 'output': 5}
                    ]
                },
                {
                    'id': 'i2',
                    'titulo': 'Lista de números pares',
                    'descripcion': 'Crea una función que retorne solo los números pares de una lista',
                    'dificultad': 3,
                    'puntos': 20,
                    'codigo_plantilla': '''def filtrar_pares(lista):
    # Escribe tu código aquí
    pass

# Prueba
numeros = [1, 2, 3, 4, 5, 6, 7, 8]
pares = filtrar_pares(numeros)
print(pares)  # [2, 4, 6, 8]''',
                    'pistas': [
                        'Crea una lista vacía para almacenar los pares',
                        'Recorre la lista original con un for',
                        'Si el número es par (numero % 2 == 0), agrégalo a la nueva lista'
                    ],
                    'tests': [
                        {'input': [1,2,3,4,5,6], 'output': [2,4,6]},
                        {'input': [10,15,20,25], 'output': [10,20]}
                    ]
                },
                {
                    'id': 'i3',
                    'titulo': 'Diccionario de estudiantes',
                    'descripcion': 'Crea una función que agregue un estudiante a un diccionario',
                    'dificultad': 4,
                    'puntos': 25,
                    'codigo_plantilla': '''def agregar_estudiante(diccionario, nombre, edad, nota):
    # Escribe tu código aquí
    pass

# Prueba
estudiantes = {}
agregar_estudiante(estudiantes, "Ana", 20, 95)
agregar_estudiante(estudiantes, "Luis", 22, 88)
print(estudiantes)''',
                    'pistas': [
                        'Usa el nombre como clave del diccionario',
                        'El valor debe ser otro diccionario con edad y nota',
                        'Ejemplo: diccionario[nombre] = {"edad": edad, "nota": nota}'
                    ],
                    'tests': []
                },
                {
                    'id': 'i4',
                    'titulo': 'Promedio de una lista',
                    'descripcion': 'Crea una función que calcule el promedio de una lista de números',
                    'dificultad': 3,
                    'puntos': 20,
                    'codigo_plantilla': '''def calcular_promedio(numeros):
    # Escribe tu código aquí
    pass

# Prueba
notas = [85, 90, 78, 92, 88]
promedio = calcular_promedio(notas)
print(f"Promedio: {promedio}")''',
                    'pistas': [
                        'Usa sum() para sumar todos los números',
                        'Usa len() para contar cuántos números hay',
                        'Divide la suma entre la cantidad: sum(numeros) / len(numeros)'
                    ],
                    'tests': [
                        {'input': [10,20,30], 'output': 20},
                        {'input': [85,90,95], 'output': 90}
                    ]
                }
            ],
            'avanzado': [
                {
                    'id': 'a1',
                    'titulo': 'Clase Calculadora',
                    'descripcion': 'Implementa una clase Calculadora con métodos para operaciones básicas',
                    'dificultad': 5,
                    'puntos': 30,
                    'codigo_plantilla': '''class Calculadora:
    def __init__(self):
        # Constructor
        pass
    
    def sumar(self, a, b):
        # Implementa suma
        pass
    
    def restar(self, a, b):
        # Implementa resta
        pass
    
    def multiplicar(self, a, b):
        # Implementa multiplicación
        pass
    
    def dividir(self, a, b):
        # Implementa división (maneja división por cero)
        pass

# Prueba
calc = Calculadora()
print(calc.sumar(10, 5))
print(calc.dividir(10, 2))''',
                    'pistas': [
                        'Cada método debe retornar el resultado de la operación',
                        'En dividir, verifica que b no sea 0 antes de dividir',
                        'Usa if b == 0: return "Error" o raise ValueError'
                    ],
                    'tests': []
                },
                {
                    'id': 'a2',
                    'titulo': 'Clase Estudiante',
                    'descripcion': 'Crea una clase Estudiante con atributos y método para calcular promedio',
                    'dificultad': 5,
                    'puntos': 30,
                    'codigo_plantilla': '''class Estudiante:
    def __init__(self, nombre, edad):
        # Inicializa atributos
        self.nombre = nombre
        self.edad = edad
        self.notas = []
    
    def agregar_nota(self, nota):
        # Agrega una nota a la lista
        pass
    
    def calcular_promedio(self):
        # Calcula y retorna el promedio de las notas
        pass
    
    def mostrar_info(self):
        # Muestra información del estudiante
        pass

# Prueba
est = Estudiante("María", 20)
est.agregar_nota(90)
est.agregar_nota(85)
est.agregar_nota(95)
print(est.calcular_promedio())
est.mostrar_info()''',
                    'pistas': [
                        'agregar_nota debe hacer: self.notas.append(nota)',
                        'calcular_promedio: sum(self.notas) / len(self.notas)',
                        'mostrar_info debe usar print para mostrar nombre, edad y promedio'
                    ],
                    'tests': []
                },
                {
                    'id': 'a3',
                    'titulo': 'Decorador de tiempo',
                    'descripcion': 'Crea un decorador que mida el tiempo de ejecución de una función',
                    'dificultad': 7,
                    'puntos': 40,
                    'codigo_plantilla': '''import time

def medir_tiempo(funcion):
    def wrapper(*args, **kwargs):
        # Implementa el decorador aquí
        pass
    return wrapper

@medir_tiempo
def funcion_lenta():
    time.sleep(1)
    print("Función ejecutada")

# Prueba
funcion_lenta()''',
                    'pistas': [
                        'Guarda el tiempo inicial: inicio = time.time()',
                        'Ejecuta la función: resultado = funcion(*args, **kwargs)',
                        'Calcula tiempo transcurrido: time.time() - inicio',
                        'Imprime el tiempo y retorna el resultado'
                    ],
                    'tests': []
                }
            ]
        }
    
    def obtener_ejercicios_por_nivel(self, nivel):
        """Retorna todos los ejercicios de un nivel"""
        return self.ejercicios.get(nivel, self.ejercicios['principiante'])
    
    def obtener_ejercicio(self, ejercicio_id):
        """Obtiene un ejercicio específico por su ID"""
        for nivel, ejercicios in self.ejercicios.items():
            for ejercicio in ejercicios:
                if ejercicio['id'] == ejercicio_id:
                    return ejercicio
        return None
    
    def obtener_ejercicio_aleatorio(self, nivel):
        """Retorna un ejercicio aleatorio del nivel especificado"""
        import random
        ejercicios_nivel = self.ejercicios.get(nivel, [])
        if ejercicios_nivel:
            return random.choice(ejercicios_nivel)
        return None
    
    def contar_ejercicios(self):
        """Cuenta total de ejercicios por nivel"""
        return {
            nivel: len(ejercicios) 
            for nivel, ejercicios in self.ejercicios.items()
        }
