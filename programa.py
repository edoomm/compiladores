from AFN import *
import copy

idsAfns = 0 # Servirá para asignar IDs a los AFNs que vayan siendo creados
AFNs = {} # Servirá para ir guardando los AFNs creados
analizador = AnalizadorLexico()

def esperar(msj = None):
    """Muestra un mensaje de espera antes de pasar a una acción siguiente

    Args:
        msj (str, optional): El mensaje que se quisiera ver para la espera. Defaults to None.
    """
    if msj == None:
        input("Presione cualquier letra para continuar...")
    else:
        input(msj)

def error(msj = None):
    """Imprime un mensaje de error

    Args:
        msj (str): Mensaje adicional a agregar al error
    """
    if msj == None:
        print("ERROR")
    else:
        print("ERROR:", msj)

def imprimirMenu():
    """Imprime el menú del programa principal
    """
    print("Menu")
    print("---------------")
    print("1) Crear AFN básico")
    print("2) Unir AFNs")
    print("3) Concatenar AFNs")
    print("4) Cerradura positiva")
    print("5) Cerradura de Kleene")
    print("6) Opcional")
    print("7) Unión para Analizador Léxico")
    print("8) Convertir AFN a AFD")
    print("9) Analizar una cadena")
    print("10) Eliminar AFN de la lista de AFNs")
    print("\n0) Salir")

def leerCaracter(msj):
    """Lee un caracter. Si el usuario ingresa una cadena, solo se tomará en cuenta el primer caracter de la cadena

    Args:
        msj (str): Mensaje adicional a agregar al error

    Returns:
        chr: El caracter leido
    """
    s = input(msj)
    if len(s) > 1:
        print("Solo se tomará el primer caracter de su cadena")
    
    return s[0]

def leerID(msj, end=None):
    """Lee un ID valido de la lista de AFNs que se tiene

    Args:
        msj (str): El mensaje que se despliega en la función input()
        end (str, optional): El caracter con el que puede terminar la lectura de un ID. Defaults to None

    Returns:
        int: El ID valido
    """
    id = input(msj)
    try:
        id = int(id)
        if id == end: # Acaba la lectura
            return -1
    except:
        pass

    if id not in AFNs.keys():
        print("ID no valido, vuelva a intentarlo")
        return leerID(msj)

    return id

def imprimirAFNs():
    """Imprime la lista de AFNs disponibles
    """
    print(list(AFNs.keys()))

def guardarAFN(afn):
    """Guarda en el diccionario de AFNs un AFN

    Args:
        afn (AFN): El AFN a aguardar
    """
    id = input("Ingrese un ID para identificar el AFN creado\n(Si no ingresa nada, el AFN será guardado con un número)\nID: ")
    if not id:
        AFNs[idsAfns] = afn
    else:
        # Se verifica si el ID es un número y si también no ya existe en los IDs
        try:
            idnum = int(id)
            if idnum < 0:
                print("No se puede usar un ID negativo, vuelva a intentar con otro ID")
                guardarAFN(afn)
                return
            else:
                id = idnum
        except:
            pass
        if id in AFNs.keys():
            print("El ID ingresado ya existe, vuelva a intentar con otro ID")
            guardarAFN(afn)
            return
        
        afn.idAFN = id
        AFNs[id] = afn

# Opción 1
def crearAfnBasico():
    """Opción del menú para que el usuario pueda crear un AFN básico
    """
    s1 = leerCaracter("Ingrese el simbolo inferior: ")
    s2 = leerCaracter("Ingrese el simbolo superior: ")

    if ord(s1) > ord(s2):
        error("En la lectura de los caractéres. El caracter inferior es superior al caracter superior")
        return

    global idsAfns
    a = AFN(idsAfns)
    a.crearAFNBasico(s1, s2)

    print("AFN con ID", a.idAFN, "creado con éxito")
    idsAfns += 1

    guardarAFN(a)

# Opción 2
def unirAFNs(id1, id2):
    """Une a través de 2 IDs dados de AFNs a el primer AFN

    Args:
        id1 (int): El ID del primer AFN al que se le hará la unión
        id2 (int): El ID del segundo AFN
    """
    aux = copy.deepcopy(AFNs[id2])
    AFNs[id1].unir(aux)
    print("Unión guardada en AFN con ID", id1)

# Opción 3
def concatenarAFNs(id1, id2):
    """Concatena 2 AFNs en un AFN

    Args:
        id1 (int): El ID del AFN al que se le pegará la concatenación
        id2 (int): El ID del segundo AFN
    """
    aux = copy.deepcopy(AFNs[id2])
    AFNs[id1].concatenar(aux)
    print("Concatenación guardada en AFN con ID", id1)

# Opción 4
def cerradurapositivaAFN(id):
    """Cerradura positiva de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su cerradura positiva
    """
    AFNs[id].cerradurap()
    print("Cerradura positiva hecha con éxito a AFN con ID", id)

# Opción 5
def cerradurakleneeAFN(id):
    """Cerradura Kleene de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su cerradura Kleene
    """
    AFNs[id].cerradurak()
    print("Cerradura Kleene hecha con éxito a AFN con ID", id)

# Opción 6
def opcionalAFN(id):
    """Opcional de un AFN. Operación '?' de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su opcional
    """
    AFNs[id].opcional()
    print("Opcional hecho con éxito a AFN con ID", id)

# Opción 7
def unionanlex():
    """Realiza la construcción del analizador léxico a través de la unión de diferentes AFNs
    """
    lst = [] # Lista donde se guardarán los AFNs a unir
    id = 0
    while id != -1:
        print("AFNs escogidos:\n", lst)
        print("Escoja un ID de los AFNs disponibles (termine con '-1'):")
        imprimirAFNs()
        id = leerID("ID: ", "-1")
        if id == -1:
            break
        lst.append(id)
        lst = list(set(lst)) # Remueve duplicados

    # Se unen y crean el analizador léxico
    if analizador.union([AFNs[i] for i in lst]) != None:
        print("Analizador léxico creado correctamente")

def menu(op):
    """Función que sirve para esocger la acción que el usuario desea realizar

    Args:
        op (int): La opción escojida por el usuario
    """
    if op == 1:
        crearAfnBasico()
    elif op == 2 or op == 3:
        if len(AFNs) < 2:
            print("Debe ingresar al menos 2 AFNs con los que se puedan unir entre ellos")
        else:
            print("Escoja 2 IDs diferentes de los AFNs disponibles que han sido creados:")
            imprimirAFNs()
            id1 = leerID("Ingrese el ID del primer AFN: ")
            id2 = leerID("Ingrese el ID del segundo AFN: ")
            # Se validan que los IDs sean diferentes
            if id1 != id2:
                if op == 2:
                    unirAFNs(id1, id2)
                else:
                    concatenarAFNs(id1, id2)
            else:
                print("Los IDs deben ser distintos. No se ha hecho ninguna unión")
    elif 3 < op < 7 or op == 8:
        if len(AFNs) < 1:
            print("Debe haber creado por lo menos un AFN")
        else:
            print("Escoja un ID de los AFNs disponibles que han sido creados:")
            imprimirAFNs()
            id = leerID("Ingrese el ID del AFN: ")
            if op == 4:
                cerradurapositivaAFN(id)
            elif op == 5:
                cerradurakleneeAFN(id)
            elif op == 6:
                opcionalAFN(id)
            elif op == 8:
                # TODO: Conversión de AFN a AFD
                pass
    elif op == 7:
        if len(AFNs) < 2:
            print("Debe ingresar al menos 2 AFNs con los que se puedan unir entre ellos")
        else:
            unionanlex()
    elif op == 10:
        if len(AFNs) < 1:
            print("No se tiene ningun AFN guardado")
        else:
            print("Escoja el ID del AFN a eliminar")
            imprimirAFNs()
            id = leerID("Ingrese el ID (Para cancelar la operación, ingrese -1)\nID:", -1)
            if id != -1:
                del AFNs[id]
                print("AFN con ID", id, " quitado de la lista")
    elif op == 0:
        print("(:")
        return
    else:
        error("Opción no valida. Vuelva a intentarlo")

    esperar()

def main():
    """Función principal que hace correr el programa
    """
    op = -1
    while op != 0:
        imprimirMenu()
        op = int(input("Su opción: "))
        menu(op)

main()