### Clase/s ###

import datetime
import json
from typing import List, Optional

class Tarea():
    file_path = 'tareas.json' # Archivo para almacenar las tareas

    # Constructor con nombre como parametro de entrada, __marcada esta por defecto en False y recoge el momento de crearla
    def __init__(self, nombre:str, momento_creada: Optional[datetime.datetime] = None, marcada: bool = False) -> None: 
        self.id: int = self.generar_id()
        self.nombre: str = nombre  # Nombre que recibe la tarea
        self._marcada: bool = marcada # nos indica si esta completada o no, por defecto al crear una tarea no estara completada.
        self.__momento_creada: datetime.datetime = momento_creada or datetime.datetime.now() # Momento de crearla, la usaremos para ordenar la lista de tareas

    def __str__(self) -> str: # Podemos comprobar el estado de una tarea de manera aislada
        estado = 'Completada' if self._marcada else 'No completada'
        return f'Tarea {self.id}: {self.nombre}, {estado}, creada en el momento {str(self.__momento_creada)}'
    def get_marcada(self) -> bool: # Devuelve el booleano segun este la tarea, por defecto False
        return self._marcada
    
    def set_marcada(self, marca:bool=True) -> None: # Tiene un booleando como entrada y no devuelve nada, nos permite cambiar el estado de la tarea
        self._marcada = marca # modifica el valor de si esta marcada o no
        self.set_momento_creada() # Cambia el momento creada, lo actualiza
        self.guardar_tareas() # Ejecuta la funcion que guarda la informacion en las tareas
      
    def get_momento_creada(self) -> str: # Podemos ver el momento en el que se creó la tarea originalmente
        return str(self.__momento_creada) # Hacemos que devuelva un string para visualizarlo, pero sigue siendo un objeto datetime para trabajar con el
    
    def set_momento_creada(self) -> None: # Modifica el momento de creacion
        self.__momento_creada = datetime.datetime.now()            

    def eliminar(self) -> None:
        tareas = Tarea.cargar_tareas()
        tareas = [tarea for tarea in tareas if tarea['nombre'] != self.nombre] # Realiza un bucle en el que compara el nombre de la tarea en el archivo
        for idx, tarea in enumerate(tareas):
            tarea['id'] = idx + 1
        Tarea.guardar_tareas_dic(tareas)
    
    def guardar_tareas(self) -> None:
        tareas = Tarea.cargar_tareas()
        for tarea in tareas:
            if tarea['nombre'].strip().lower() == self.nombre.strip().lower(): # comprueba que la tarea existe y la actualiza
                tarea['momento_creada'] = self.get_momento_creada()
                tarea['marcada'] = self.get_marcada()
                tarea['nombre'] = self.nombre 
                break
        else: 
            tareas.append({ # si la tarea no existe previamente, la crea y la introduce
                'id': self.id,
                'nombre': self.nombre,
                'momento_creada': self.get_momento_creada(),
                'marcada': self.get_marcada()
            })
        Tarea.guardar_tareas_dic(tareas)

    @classmethod
    def generar_id(cls) -> int: # Genera un id a cada tarea que mostraremos al imprimir
        tareas = cls.cargar_tareas()
        if not tareas:
            return 1
        return max(tarea['id'] for tarea in tareas) +1
    
    @classmethod
    def buscar_tarea_por_nombre(cls, nombre:str) -> Optional['Tarea']: 
        tareas = cls.cargar_tareas()
        for tarea_data in tareas: 
            if tarea_data['nombre'].strip().lower() == nombre.strip().lower(): # Modifica los strings para hacer una comparacion correcta
                return Tarea(
                    nombre=tarea_data['nombre'],
                    momento_creada = datetime.datetime.fromisoformat(tarea_data['momento_creada']),
                    marcada = tarea_data['marcada']
                ) # Si la que buscamos se encuentra en el archivo json, devuelve la tarea
        return None
    
    @classmethod
    def cargar_tareas(cls) -> List[dict]:
        try:
            with open(cls.file_path, 'r') as file: # lee el archivo json y toma las tareas, si no existe el archivo devuelve una lista vacia
                return json.load(file)
        except FileNotFoundError:
            return []
        
    @classmethod
    def guardar_tareas_dic(cls, tareas: List[dict]) -> None: # Guarda las tareas en el archivo json
        with open(cls.file_path, 'w') as file:
            json.dump(tareas, file, indent=4)
    
class Consola():

    # Constructor
    def __init__(self) -> None:
        self.opciones = {
            '1': self.opcion_uno,
            '2': self.opcion_dos,
            '3': self.menu_opcion_tres,
            '4': self.opcion_cuatro,
            'q': self.quit
        }
        self.running = True

    ### Displays
    # Display principal
    def display_menu_principal(self) -> None: # funcion que muestra el menu principal 
        print('Bienvenido a la lista de tareas!')
        imprimir_lista()
        print('Opciones:')
        print('1. Añadir nueva tarea')
        print('2. Completar una tarea')
        print('3. Editar una tarea')
        print('4. Eliminar una tarea')
        print('q. Quit')

    # Display opcion 3
    def display_menu_opcion_tres(self) -> None: # Funcion que muestra un menu al entrar en opcion 3
        imprimir_lista()
        print('Menú de edición de tareas')
        print('1. Ver informacion de una tarea')
        print('2. Cambiar nombre a una tarea')
        print('3. Desmarcar una tarea')
        print('4. Volver al menu principal') # Opcion para volver al menu principal

    ### Logica
    # Logica principal
    def run(self) -> None:
        while self.running:
            self.display_menu_principal()
            eleccion:str = input('Elige una opcion: ').lower() # Pide que elijas una opcion como input
            accion = self.opciones.get(eleccion) # Selecciona el atributo que queremos dentro de opciones
            if accion: # Esto es lo mismo que poner accion == True
                accion()
            else:
                print(f'Elección errónea: {eleccion}') # Solo aparece si la opcion es erronea

    # Logica Opcion 1
    def opcion_uno(self) -> None: # Menu de eleccion para añadir tareas
        self.anadir_tarea() 

    def anadir_tarea(self) -> Tarea:
        nombre: str = input('Introduce una nueva tarea: ') # Se introduce el nombre por consola. siempre sera un string
        if nombre == '':
            print('Por favor, introduce un nombre válido')
        else:
            nueva_tarea:Tarea = Tarea(nombre=nombre) # Crea la tarea, la cual se introduce en la lista debido a nuestro constructor
            nueva_tarea.guardar_tareas()
            print(f'La tarea "{nombre}" ha sido añadida con ID {nueva_tarea.id}.') # Muestra la tarea recien introducida
            return nueva_tarea # Devuelve la tarea para poder trabajar con ella, por ejemplo usando los metedos o cambiandole el nombre

    # Logica Opcion 2
    def opcion_dos(self) -> None: # Marcado de la tarea 
        nombre: str = input('Introduce el nombre de la tarea a marcar: ')
        tarea = Tarea.buscar_tarea_por_nombre(nombre)
        if tarea:
            tarea.set_marcada() # Por default a True
            print(f'La tarea "{nombre}" ha sido marcada como completada.')
        else:
            print(f'No se encontró la tarea con el nombre "{nombre}".')
    
    # Logica Opcion 3
    def menu_opcion_tres(self) -> None:
        while True:
            self.display_menu_opcion_tres()
            eleccion:str = input('Elige una opcion: ').lower()
            if eleccion == '1': # Si la eleccion es marcar la tarea, llama al metodo marcar_tarea_completada creada abajo
                self.mostrar_info_tarea()
            elif eleccion == '2':
                self.cambiar_nombre_tarea()
            elif eleccion == '3':
                self.desmarcar_tarea_completada()  
            elif eleccion == '4': # Si la eleccion es volver, vuelve al menu principal
                return 
            else:
                print(f'Eleccion erronea: {eleccion}')
            
    def mostrar_info_tarea(self) -> None: # Muestra la informacion de la tarea accediendo a ella tanto por atributo como por metodos
        nombre: str = input('Introduce el nombre de la tarea a mostrar: ') 
        tarea = Tarea.buscar_tarea_por_nombre(nombre)
        if tarea != None:
            print(f'Nombre: {tarea.nombre}')
            print(f'Momento creada: {tarea.get_momento_creada()}')
            print(f'Marcada: {tarea.get_marcada()}')
        else:
            print(f'No se encontró la tarea con el nombre "{nombre}".')

    def cambiar_nombre_tarea(self) -> None:
        nombre: str = input('Introduce el nombre de la tarea a cambiar: ')
        tarea = Tarea.buscar_tarea_por_nombre(nombre)
        if tarea != None:
            nuevo_nombre: str = input('Introduce el nuevo nombre de la tarea: ') # Aqui introducimos el nombre nuevo para guardarlo
            if Tarea.buscar_tarea_por_nombre(nuevo_nombre):
                print(f'Ya existe una tarea con el nombre "{nuevo_nombre}".')
                return    
                   
            tareas = Tarea.cargar_tareas()
            for tarea_data in tareas:
                if tarea_data['nombre'].strip().lower() == nombre.strip().lower():
                    tarea_data['nombre'] = nuevo_nombre
                    tarea.nombre = nuevo_nombre
                    Tarea.guardar_tareas_dic(tareas)
                    print(f'El nombre de la tarea ha sido modificado a "{nuevo_nombre}"')
                    return
        else:
            print(f'No se encontró la tarea con el nombre "{nombre}".')

    def desmarcar_tarea_completada(self) -> None: # Encuentra la tarea por nombre y modifica con el metodo set_marcada a False
        nombre: str = input('Introduce el nombre de la tarea a desmarcar: ')
        tarea = Tarea.buscar_tarea_por_nombre(nombre)
        if tarea != None:
            tarea.set_marcada(False)
            print(f'La tarea "{nombre}" ha sido desmarcada, ahora está no completada.')
        else:
            print(f'No se encontró la tarea con el nombre "{nombre}".')

    # Logica Opcion 4
    def opcion_cuatro(self) -> None:
        imprimir_lista()
        self.eliminar_tarea()
    
    def eliminar_tarea(self) -> None:
        nombre: str = input('Introduce el nombre de la tarea a eliminar: ')
        tarea = Tarea.buscar_tarea_por_nombre(nombre)
        if tarea != None:
            tarea.eliminar() # Llama al metodo eliminar para sacar la tarea de la lista de tareas
            print(f'La tarea "{nombre}" ha sido eliminada, ya no existe.')
        else:
            print(f'No se encontró la tarea con el nombre "{nombre}".')

    # Logica Salir
    def quit(self) -> None:
        print('Salir del programa.')
        self.running = False

### Funciones ###
### -----------------------------------------------------------------------------------------------------------------------------###
def casilla(tar:Tarea) -> None: # Añade una marca al nombre para indicar si esta completada o no
    estado = '[X]' if tar.get_marcada() else '[ ]'
    print(f'{estado} {tar.id}. {tar.nombre}')

def orden_lista(obj_list:List[dict]) -> List[dict]: 
    sorted_obj_list = sorted(obj_list, key=lambda obj: obj['momento_creada']) # Ordena la lista de tareas, en funcion del momento de crearla o modificarla
    return sorted_obj_list # Devuelve la lista ordenada
 
def imprimir_lista(): # Carga el archivo Json, toma la lista ordenada de la funcion orden lista y a cada elemento de la lista muestra la tarea, con la info del archivo
    tareas = Tarea.cargar_tareas() 
    for tarea_data in orden_lista(tareas): # Imprime las tareas, mostrando si estan marcadas o no
        tarea = Tarea(
            nombre = tarea_data['nombre'],
            momento_creada=datetime.datetime.fromisoformat(tarea_data['momento_creada']),
            marcada=tarea_data['marcada'],
            
        )
        tarea.id = tarea_data['id']
        casilla(tarea)


if __name__ == '__main__':
    consola = Consola()
    consola.run() 