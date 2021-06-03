from convertidorPostfijo import *
import copy

idsAfns = 0 # Servirá para asignar IDs a los AFNs que vayan siendo creados
afns = {} # Servirá para ir guardando los AFNs creados
analizador = AnalizadorLexico()
afds = {} # Guardará los AFDs
idsAfds = 0 # Servirá para asignar IDs a los AFDs que vayan siendo creados

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

def imprimirmenu():
    """Imprime el menú principal del programa
    """
    linebreak = "\n"
    for i in range(0, 8):
        linebreak += "\n"
    print(linebreak)
    print("Menú principal")
    print("--------------")
    print("1) AFNs")
    print("2) Analizador sintáctico")

    print("\n0) Salir")

def leerCaracter(msj):
    """Lee un caracter. (Si el usuario ingresa una cadena, solo se tomará en cuenta el primer caracter de la cadena)

    Args:
        msj (str): Mensaje adicional a agregar al error

    Returns:
        chr: El caracter leido
    """
    return input(msj)
    # if len(s) > 1:
    #     print("Solo se tomará el primer caracter de su cadena")
    
    # return s[0]

def leerID(msj, end=None, afs=afns):
    """Lee un ID valido de la lista de AFNs que se tiene

    Args:
        msj (str): El mensaje que se despliega en la función input()
        end (str, optional): El caracter con el que puede terminar la lectura de un ID. Defaults to None
        afs (AFN|AFD, optional): Puede leer el ID del diccionario de afns o afds. Defaults to afns

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

    if id not in afs.keys():
        print("ID no valido, vuelva a intentarlo")
        return leerID(msj)

    return id

def imprimirAFs(afs=afns):
    """Se imprime los Autómatas Finitos, ya sean deterministas o no deterministas

    Args:
        afs (AFN|AFD, optional): El tipo de Autómata Finito a imprimir. Defaults to afns.
    """
    print(str(list(afs.keys())).replace('\'', ''))

def guardarAFN(afn):
    """Guarda en el diccionario de AFNs un AFN

    Args:
        afn (AFN): El AFN a aguardar
    """
    id = input("Ingrese un ID para identificar el AFN creado\n(Si no ingresa nada, el AFN será guardado con un número)\nID: ")
    if not id:
        afns[idsAfns] = afn
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
        if id in afns.keys():
            print("El ID ingresado ya existe, vuelva a intentar con otro ID")
            guardarAFN(afn)
            return
        
        afn.idAFN = id
        afns[id] = afn

def guardarAFD(afd):
    """Guarda en el diccionario de AFDs un AFD

    Args:
        afd (AFD): El AFD a aguardar
    """
    id = input("Ingrese un ID para identificar el AFD creado\n(Si no ingresa nada, el AFD será guardado con un número)\nID: ")
    if not id:
        afds[idsAfds] = afd
    else:
        # Se verifica si el ID es un número y si también no ya existe en los IDs
        try:
            idnum = int(id)
            if idnum < 0:
                print("No se puede usar un ID negativo, vuelva a intentar con otro ID")
                guardarAFD(afd)
                return
            else:
                id = idnum
        except:
            pass
        if id in afds.keys():
            print("El ID ingresado ya existe, vuelva a intentar con otro ID")
            guardarAFD(afd)
            return
        
        afds[id] = afd

def leerarchivo():
    """Lee el nombre de un archivo que será el AFD que utilizará el Analizador Léxico

    Returns:
        bool: False - Si no se pudo leer correctamente el archivo
    """
    global analizador
    aux = analizador
    try:
        aux = AnalizadorLexico(input("Ingrese el nombre del archivo de donde se obtendrá el AFD que el analizador léxico utilizará:\n"))
    except:
        print("No se pudo crear el analizador léxico correctamente. Intentelo nuevamente o con un archivo diferente")
        return False
    
    analizador = aux

def setanalizador():
    """Establece el analizador léxico que deberá usar el programa
    """
    global analizador
    if analizador.archivo == None:
        if leerarchivo() == False:
            return False
    else:
        print("Archivo que se está utilizando para analizar cadenas:", analizador.archivo + ".txt")
        newfile = input("Si quiere cambiar a un archivo diferente, escriba el nombre del archivo (Si da ENTER sin teclear nada se seguirá usando el mismo archivo):\n")
        if newfile:
            if leerarchivo() == False:
                print("Se usará el archivo", analizador.archivo, "para el analisis")
    return True

### Menu AFNs
def imprimirMenuAfns():
    """Imprime el menú de las operaciones que se pueden realizar con AFNs.
    Corresponde a la entrega del primer parcial
    """
    print("Menu AFNs")
    print("---------------")
    print("1) Crear AFN básico")
    print("2) Unir AFNs")
    print("3) Concatenar AFNs")
    print("4) Cerradura positiva")
    print("5) Cerradura de Kleene")
    print("6) Opcional")
    print("7) Unión especial")
    print("8) Convertir AFN a AFD")
    print("9) Analizar una cadena")
    print("10) Mostrar AFNs y AFDs disponibles")
    print("11) Imprimir AFD")
    print("12) Eliminar AFN de la lista de AFNs")
    print("13) Eliminar AFD de la lista de AFDs")
    print("14) Exportar AFD")
    print("\n0) Salir")

## Opción 1
def crearAfnBasico():
    """Opción del menú para que el usuario pueda crear un AFN básico
    """
    s1 = leerCaracter("Ingrese el simbolo inferior: ")
    s2 = leerCaracter("Ingrese el simbolo superior: ")

    if len(s1) == 1 and len(s2) == 1:
        if ord(s1) > ord(s2):
            error("En la lectura de los caractéres. El caracter inferior es superior al caracter superior")
            return

    global idsAfns
    a = AFN(idsAfns)
    a.crearAFNBasico(s1, s2)
    idsAfns += 1

    guardarAFN(a)

## Opción 2
def unirAFNs(id1, id2):
    """Une a través de 2 IDs dados de AFNs a el primer AFN

    Args:
        id1 (int): El ID del primer AFN al que se le hará la unión
        id2 (int): El ID del segundo AFN
    """
    aux = copy.deepcopy(afns[id2])
    afns[id1].unir(aux)
    print("Unión guardada en AFN con ID", id1)

## Opción 3
def concatenarAFNs(id1, id2):
    """Concatena 2 AFNs en un AFN

    Args:
        id1 (int): El ID del AFN al que se le pegará la concatenación
        id2 (int): El ID del segundo AFN
    """
    aux = copy.deepcopy(afns[id2])
    afns[id1].concatenar(aux)
    print("Concatenación guardada en AFN con ID", id1)

## Opción 4
def cerradurapositivaAFN(id):
    """Cerradura positiva de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su cerradura positiva
    """
    afns[id].cerradurap()
    print("Cerradura positiva hecha con éxito a AFN con ID", id)

## Opción 5
def cerradurakleneeAFN(id):
    """Cerradura Kleene de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su cerradura Kleene
    """
    afns[id].cerradurak()
    print("Cerradura Kleene hecha con éxito a AFN con ID", id)

## Opción 6
def opcionalAFN(id):
    """Opcional de un AFN. Operación '?' de un AFN

    Args:
        id (int): El ID del AFN al que se le hará su opcional
    """
    afns[id].opcional()
    print("Opcional hecho con éxito a AFN con ID", id)

## Opción 7
def unionanlex():
    """Realiza la construcción del analizador léxico a través de la unión de diferentes AFNs
    """
    lst = [] # Lista donde se guardarán los AFNs a unir
    id = 0
    while id != -1:
        print("AFNs escogidos:\n", lst)
        print("Escoja un ID de los AFNs disponibles (termine con -1):")
        imprimirAFs()
        id = leerID("ID: ", -1)
        if id == -1:
            break
        lst.append(id)
        lst = list(set(lst)) # Remueve duplicados

    # Se unen y crean el analizador léxico
    analizador.union([afns[i] for i in lst])
    if analizador.afn != None:
        print("Unión especial realizada correctamente")
        guardarAFN(copy.deepcopy(analizador.afn))
    else:
        print("No se pudo realizar la unión especial")

## Opción 8
def conversion(afn):
    """Se realiza la conversión de AFN a AFD que se guardará en un nuevo AFD

    Args:
        afn (AFN): El AFN a convertir a AFD
    """
    a = AFD(afn)
    # Se guarda
    global idsAfds
    idsAfds += 1
    guardarAFD(a)

## Opción 9
def analizarcad():
    setanalizador()
    
    analizador.CadenaSigma = input("Ingrese la cadena a analizar: ")
    print("INICIO DEL ANÁLISIS\n-----")
    analizador.analizarCadena()
    print("-----\nFIN DEL ANÁLISIS")

## Opción 10
def imprimirAFNSyAFDs():
    """Imprime los Autómatas Finitos, tanto deterministas como no deterministas que se han creado a lo largo del programa
    """
    print("AFNs")
    imprimirAFs()
    print("AFDs")
    imprimirAFs(afds)

## Opción 11
def imprimirAFD():
    """Imprime un AFD del diccionario de AFDs. (Operación cancelable)
    """
    print("AFDs")
    imprimirAFs(afds)
    id = leerID("Escoja el ID del AFD a imprimir (cancele con -1): ", end=-1, afs=afds)
    if id != -1:
        print(afds[id])

## Opción 12 y 13
def eliminarAF(afs=afns):
    """Da la opción de elimnar un AFN del diccionario de AFNs creados
    """
    print("Escoja el ID del AFN a eliminar")
    imprimirAFs(afs)
    id = leerID("Ingrese el ID (Para cancelar la operación, ingrese -1)\nID:", -1, afs=afs)
    if id != -1:
        del afs[id]
        print("AFN con ID", id, " quitado de la lista")

def menuafns(op):
    """Función que sirve para esocger la acción que el usuario desea realizar en el Menu correspondiente a los AFNs

    Args:
        op (int): La opción escojida por el usuario
    """
    if op == 1:
        crearAfnBasico()
    elif op == 2 or op == 3:
        if len(afns) < 2:
            print("Debe ingresar al menos 2 AFNs con los que se puedan unir entre ellos")
        else:
            print("Escoja 2 IDs diferentes de los AFNs disponibles que han sido creados:")
            imprimirAFs()
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
        if len(afns) < 1:
            print("Debe haber creado por lo menos un AFN")
        else:
            print("Escoja un ID de los AFNs disponibles que han sido creados:")
            imprimirAFs()
            id = leerID("Ingrese el ID del AFN: ")
            if op == 4:
                cerradurapositivaAFN(id)
            elif op == 5:
                cerradurakleneeAFN(id)
            elif op == 6:
                opcionalAFN(id)
            elif op == 8:
                conversion(afns[id])
                pass
    elif op == 7:
        if len(afns) < 2:
            print("Debe ingresar al menos 2 AFNs con los que se puedan unir entre ellos")
        else:
            unionanlex()
    elif op == 9:
        analizarcad()
    elif op == 10:
        imprimirAFNSyAFDs()
    elif op == 11:
        if len(afds) < 1:
            print("No se ha creado ningún AFD")
        else:
            imprimirAFD()
    elif op == 12:
        if len(afns) < 1:
            print("No se tiene ningun AFN guardado")
        else:
            eliminarAF(afns)
    elif op == 13:
        if len(afds) < 1:
            print("No se tiene ningun AFD guardado")
        else:
            eliminarAF(afds)
    elif op == 14:
        # TODO: Exportar AFD
        pass
    elif op == 0:
        print("Regresando a menú principal(:")
        return False
    else:
        error("Opción no valida. Vuelva a intentarlo")
    
    esperar()

### Menu Analizador Sintáctico
def imprimirMenuAnSintactico():
    """Imprime el menú correspondiente a los analizadores sintácticos implementados
    """
    linebreak = "\n"
    for i in range(0, 8):
        linebreak += "\n"
    print(linebreak)
    print("Menú Analizadores sintácticos")
    print("-----------------------------")
    print("1) Evaluar expresión numérica")
    print("2) Convertidor post-fijo")
    print("\n0) Salir")

def menuansyn(op):
    """Función que sirve para esocger la acción que el usuario desea realizar en el Menu correspondiente a los AFNs

    Args:
        op (int): La opción escojida por el usuario
    """
    if op == 1:
        evaluarcalc()
    elif op == 2:
        convpostfijo()
    elif op == 0:
        print("Regresando a menu principal(:")
        return False
    else:
        error("Opción no valida. Vuelva a intentarlo")
    esperar()

## Calculadora
def evaluarcalc():
    """Evalua a través de un AFD una expresión numérica a ingresar
    """
    if setanalizador() == False:
        return
    
    analizador.CadenaSigma = input("Ingrese la expresión a evaluar: ")
    analizador.resetattributes()
    ansyntax = Evaluador(analizador)
    if ansyntax.inieval():
        print("Expresión sintácticamente correcta.\nResultado:", ansyntax.result)
    else:
        print("Expresión sintácticamente INCORRECTA")

## Notación post-fija
def convpostfijo():
    """Convierte una expresión numérica a su equivalente en notación post-fija
    """
    if setanalizador() == False:
        return

    analizador.CadenaSigma = input("Ingrese la expresión a evaluar: ")
    analizador.resetattributes()
    ansyntax = convertidorPostfijo(analizador)
    if ansyntax.ConvPostfijo():
        print("Expresión sintácticamente correcta.\nResultado:", ansyntax.getCadenaPost())
    else:
        print("Expresión sintácticamente INCORRECTA")

def menu(op):
    """Función que sirve para esocger la acción que el usuario desea realizar

    Args:
        op (int): La opción escojida por el usuario
    """
    op1 = op
    exited = True if op1 == 0 else False
    while not exited:
        if op1 == 1:
            imprimirMenuAfns()
            try:
                op2 = int(input("Su opción: "))
                if menuafns(op2) == False:
                    exited = True
            except:
                error("Opción no valida, vuelva a intentarlo...")
        elif op1 == 2:
            imprimirMenuAnSintactico()
            try:
                op2 = int(input("Su opción:"))
                if menuansyn(op2) == False:
                    exited = True
            except:
                error("Opción no valida, vuelva a intentarlo...")
        elif op1 == 0:
            exited = True
        else:
            error("Opción no valida, vuelva a intentarlo...")
            return

def main():
    """Función principal que hace correr el programa
    """
    op = -1
    while op != 0:
        imprimirmenu()
        try:
            op = int(input("Su opción: "))
            if op == 0:
                print("(:")
                return
            menu(op)
        except:
            error("Opción no valida, vuelva a intentarlo...")
            esperar()
    # analizarcad()

main()