from AFN import *

idsAfns = 0 # Servirá para asignar IDs a los AFNs que vayan siendo creados
AFNs = [] # Servirá para ir guardando los AFNs creados

def error(msj = None):
    """Imprime un mensaje de error

    Args:
        msj (str): Mensaje adicional a agregar al error
    """
    if msj == None:
        print("ERROR")
    else:
        print("ERROR:", msj)
    input("Presione cualquier letra para continuar...")

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

def menu(op):
    """Función que sirve para esocger la acción que el usuario desea realizar

    Args:
        op (int): La opción escojida por el usuario
    """
    if op == 1:
        crearAfnBasico()
    else:
        error("Opción no valida. Vuelva a intentarlo")

def main():
    """Función principal que hace correr el programa
    """
    op = -1
    while op != 0:
        imprimirMenu()
        op = int(input("Su opción: "))
        menu(op)

main()