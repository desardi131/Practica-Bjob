### Clase/s ###

import datetime
from typing import List, Optional

class Tarea():
    tareas: List['Tarea'] = [] # Lista vacia de la clase tarea, la usaremos para almacenar todos los objetos de tipo Tarea

    # Constructor con nombre como parametro de entrada, __marcada esta por defecto en False y recoge el momento de crearla
    def __init__(self, nombre) -> None: # No devuelve nada, solo crea el objeto con estas caracteristicas
        self.nombre: str = nombre  # Nombre que recibe la tarea
        self._marcada: bool = False # nos indica si esta completada o no, por defecto al crear una tarea no estara completada.
        self.__momento_creada: datetime.datetime = datetime.datetime.now() # Momento de crearla, la usaremos para ordenar la lista de tareas
        Tarea.tareas.append(self) # Añade la tarea creada a la lista

    def __str__(self) -> str: # Podemos comprobar el estado de una tarea de manera aislada
        if self._marcada == False:
            return 'La tarea: {}, No completada, creada en el momento {}'.format(self.nombre,str(self.__momento_creada))
        else:
            return 'La tarea: {}, Completada, actualizada en el momento {}'.format(self.nombre,str(self.__momento_creada))
        
    def get_marcada(self) -> bool: # Devuelve el booleano segun este la tarea, por defecto False
        return self._marcada
    
    def set_marcada(self, marca:bool=True) -> None: # Tiene un booleando como entrada y no devuelve nada, nos permite cambiar el estado de la tarea
        self._marcada = marca
        self.set_momento_creada()
      

    def get_momento_creada(self) -> str: # Podemos ver el momento en el que se creó la tarea originalmente
        return str(self.__momento_creada) # Hacemos que devuelva un string para visualizarlo, pero sigue siendo un objeto datetime para trabajar con el
    
    def set_momento_creada(self) -> None: # Modifica el momento de creacion
        self.__momento_creada = datetime.datetime.now()            

    def eliminar(self) -> None:
        if self in Tarea.tareas:
            Tarea.tareas.remove(self)

    @classmethod
    def buscar_tarea_por_nombre(cls, nombre:str) -> Optional['Tarea']: 
        
        for tarea in cls.tareas: # itera la lista que tenemos al generar una tarea
            if tarea.nombre.strip().lower() == nombre.strip().lower(): # Modifica los strings para hacer una comparacion correcta
                return tarea # Si la que buscamos se encuentra en la lista de nombres, devuelve la tarea
        return None
    
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
                print(f'Eleccion erronea: {eleccion}') # Solo aparece si la opcion es erronea

    # Logica Opcion 1
    def opcion_uno(self) -> None: # Menu de eleccion para añadir tareas
        self.anadir_tarea() 

    def anadir_tarea(self) -> Tarea:
        nombre: str = input('Introduce una nueva tarea: ') # Se introduce el nombre por consola. siempre sera un string
        nueva_tarea:Tarea = Tarea(nombre) # Crea la tarea, la cual se introduce en la lista debido a nuestro constructor
        print(f'La tarea "{nombre}" ha sido añadida.') # Muestra la tarea recien introducida
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
            tarea.nombre = nuevo_nombre
            print(f'El nombre de la tarea ha sido modificado a "{nuevo_nombre}"')
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
            del tarea # Usa la palabra designada del para eliminar la informacion en memoria
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
    if tar.get_marcada() == False:
        print(f'[ ] {Tarea.tareas.index(tar)}. {tar.nombre}')
    else:
        print(f'[X] {Tarea.tareas.index(tar)}. {tar.nombre}')

def orden_lista(obj_list:List) -> List: 
    sorted_obj_list = sorted(obj_list, key=lambda obj: obj.get_momento_creada()) # Ordena la lista de tareas, en funcion del momento de crearla o modificarla
    return sorted_obj_list # Devuelve la lista ordenada

def imprimir_lista():
    for i in orden_lista(Tarea.tareas): # Imprime las tareas, mostrando si estan marcadas o no
        casilla(i)


if __name__ == '__main__':
    consola = Consola()
    consola.run() 