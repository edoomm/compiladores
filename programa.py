from AFN import *

idsAfns = 0 # Servirá para asignar IDs a los AFNs que vayan siendo creados
AFNs = [] # Servirá para ir guardando los AFNs creados

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
    print("10) Probar analizador léxico")
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

def leerID(msj):
    """Lee un ID valido de la lista de AFNs que se tiene

    Args:
        msj (str): El mensaje que se despliega en la función input()

    Returns:
        int: El ID valido
    """
    n = "NaN"
    while not n.isdigit():
        n = input(msj)
    n = int(n)
    if not (0 <= n < len(AFNs)):
        print("Rango no valido")
        return leerID(msj)

    return n

def imprimirAFNs():
    """Imprime la lista de AFNs disponibles
    """
    l = [i for i in range(len(AFNs))]
    print(l)

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

    AFNs.append(a)

# Opción 2
def unirAFNs(id1, id2):
    """Une a través de 2 IDs dados de AFNs a el primer AFN

    Args:
        id1 (int): El ID del primer AFN al que se le hará la unión
        id2 (int): El ID del segundo AFN
    """
    AFNs[id1].unir(AFNs[id2])
    print("Unión guardada en AFN con ID", id1)

# Opción 3
def concatenarAFNs(id1, id2):
    """Concatena 2 AFNs en un AFN

    Args:
        id1 (int): El ID del AFN al que se le pegará la concatenación
        id2 (int): El ID del segundo AFN
    """
    AFNs[id1].concatenar(AFNs[id2])
    print("Concatenación guardada en AFN con ID", id1)

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
            id1 = leerID("Ingrese el ID del primer digito: ")
            id2 = leerID("Ingrese el ID del segundo digito: ")
            # Se validan que los IDs sean diferentes
            if id1 != id2:
                if op == 2:
                    unirAFNs(id1, id2)
                else:
                    concatenarAFNs(id1, id2)
            else:
                print("Los IDs deben ser distintos. No se ha hecho ninguna unión")
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