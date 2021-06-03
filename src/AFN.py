from Estado import *
from Transicion import *

# Simulación clase SimbolosEspeciales
EPSILON = chr(5)
FIN = chr(0)

class AFN():
    def __init__(self, id=0):
        self.contadorIds=0
        self.incremento=0
        self.EdoIni=None
        self.EdosAcept=set()
        self.EdosAFN=set()
        self.Alfabeto = set()
        self.idAFN = id
    
    def __str__(self):
        print("AFN con ID:", self.idAFN)
        a = list(self.Alfabeto)
        a.sort()
        return "El alfabeto es:"+ str(a)

    # OPCIÓN 1
    # AFNBasico para simbolo inferior (o superior)
    def crearAFNBasico(self,simbolo, s2=None):
        """Crea un AFN básico a partir de 1 o 2 símbolos

        Args:
            simbolo (chr): El caracter (inferior) principal que irá en el AFN
            s2 (chr, optional): El caracter superior. Defaults to None.
        """
        isonechar = True if (len(simbolo) == 1) else False
        # Se valida primero s2
        simbolo2 = simbolo
        # Esto simula la sobreescritura del método
        if s2 != None and isonechar:
            if ord(simbolo) < ord(s2):
                # Si todo es valido entonces
                simbolo2 = s2
            elif simbolo != s2:
                print("Error: Se creará un AFN con solo el primer simbolo que se dió, porque el simbolo superior es mayor que el inferior")

        # Se crea el primer estado con un id>=0
        self.incremento+=1
        e1=Estado()
        e1.setId(self.incremento)
        # Se crea el segundo estado con un id>= e1.idEstado
        e2=Estado()
        self.incremento+=1
        e2.setId(self.incremento)
        # Se crea la transición
        t=Transicion()
        t.setParametros(simbolo,simbolo2,e2)
        e2.setAceptacion(True)
        e1.setTransicion(t)

        # Se actualiza el alfabeto
        if isonechar:
            for i in range(ord(simbolo), ord(simbolo2) + 1):
                self.Alfabeto.add(chr(i))
        else:
            self.Alfabeto.add(simbolo)

        self.EdoIni=e1
        self.setEdosAFN(e1)
        self.setEdosAFN(e2)
        self.setEdosAcept(e2)
    
    # OPCIÓN 2
    def unir(self, f2):
        """Función que sirve para unir dos AFNs. Operación '|' en regex

        Args:
            f2 (AFN): El segundo AFN que se unirá al primer AFN de donde es llamada la función
        """
        e1 = Estado()
        e2 = Estado()
        # El tendrá dos transiciones epsilon. Una al edo inicial del AFN this, y otra al estado inicial de f2
        t1 = Transicion(simb1=EPSILON, edo=self.EdoIni)
        t2 = Transicion(simb1=EPSILON, edo=f2.EdoIni)
        e1._transiciones.add(t1)
        e1._transiciones.add(t2)
        # Ahora cada estado de aceptación de this y f2 tendrá una transiciíon epsilón al nuevo estado de aceptación
        # Y los estados de aceptación pasan a dejar de ser de aceptación
        for e in self.EdosAcept:
            e._transiciones.add(Transicion(simb1=EPSILON, edo=e2))
            e.aceptacion = False
        for e in f2.EdosAcept:
            e._transiciones.add(Transicion(simb1=EPSILON, edo=e2))
            e._aceptacion = False
        
        # Se actualizan ids, primero los de self y luego f2, dependiendo del número que self tenga en su ultimo ID
        self.actualizarIds(1)
        f2.actualizarIds(self.obtenerUltimoIdEstado())
        # Se actualiza la información
        self.EdosAcept.clear()
        f2.EdosAcept.clear()
        self.EdoIni = e1
        e2.aceptacion = True
        self.EdosAcept.add(e2)
        self.EdosAFN = self.EdosAFN | f2.EdosAFN
        e2.setId(self.obtenerUltimoIdEstado() + 1) # Se actualiza el ID del nuevo estado final con todos los IDs de los AFNs ya en self
        self.EdosAFN.add(e1)
        self.EdosAFN.add(e2)
        self.Alfabeto = self.Alfabeto | f2.Alfabeto

    # OPCIÓN 3
    def concatenar(self, f):
        """Fusion del estado de aceptación del AFN con el AFN f. Se conserva el estado de aceptación del AFN original

        Args:
            f (AFN): AFN f con el que será concatenado AFN
        """
        for t in f.getEdoInicial()._transiciones:
            for e in self.getEdosAcept():
                e._transiciones.add(t)
                e.aceptacion = False # Los estados de aceptación de self dejan de serlo

        # Se elimina el estado inicial de f
        f.EdosAFN.remove(f.EdoIni)
        # Se actualiza el ID de los estados de f con el número de estados que tiene self
        f.actualizarIds(len(self.EdosAFN))
        # Se actualiza self
        self.EdosAcept = f.EdosAcept
        self.EdosAFN = self.EdosAFN | f.EdosAFN
        self.Alfabeto = self.Alfabeto | f.Alfabeto

    # OPCIÓN 4
    def cerradurap(self):
        """Cerradura positiva de un AFN
        """
        # Se crea un nuevo edo inicial y final de aceptación
        ei = Estado()
        ef = Estado()

        # Se crean y añaden las transiciones epsilon
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=self.EdoIni))
        for e in self.EdosAcept:
            e._transiciones.add(Transicion(simb1=EPSILON, edo=ef))
            e._transiciones.add(Transicion(simb1=EPSILON, edo=self.EdoIni))

            e.aceptacion = False

        # Se actualizan primero los IDs de self
        self.actualizarIds(1)
        # Luego se actualiza ef
        ef.setId(self.obtenerUltimoIdEstado() + 1)
        ef.aceptacion = True
        # Y ya posterior a esto se actualiza la información de self
        self.EdoIni = ei
        self.EdosAcept.clear()
        self.EdosAcept.add(ef)
        self.EdosAFN.add(ei)
        self.EdosAFN.add(ef)

    # OPCIÓN 5
    def cerradurak(self):
        """Cerradura de Kleen de un AFN
        """
        # Se crea un nuevo estado inicial y de aceptación
        ei = Estado()
        ef = Estado()

        # Se agregan las transiciones del estado inicial
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=self.EdoIni))
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=ef))

        # Se hacen transiciones al nuevo estado de aceptación de los estados de aceptación de self
        for e in self.EdosAcept:
            e._transiciones.add(Transicion(simb1=EPSILON, edo=ef))
            e._transiciones.add(Transicion(simb1=EPSILON, edo=self.EdoIni))
            e.aceptacion = False

        # Actualización de IDs
        self.actualizarIds(1)
        ef.setId(self.obtenerUltimoIdEstado() + 1)
        # Se actualizan los nuevos estados de inicio y aceptación de self
        self.EdoIni = ei
        ef.aceptacion = True
        # Se actualiza AFN
        self.EdosAcept.clear()
        self.EdosAcept.add(ef)
        self.EdosAFN.add(ei)
        self.EdosAFN.add(ef)

    # OPCIÓN 6
    def opcional(self):
        """Operación ? para un AFN
        """
        # Se crean nuevos edos inicial y de aceptación
        ei = Estado()
        ef = Estado()

        # Se agregan las transiciones del nuevo estado inicial
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=self.EdoIni))
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=ef))
        # Se agregan las transiciones de los edos acept con el nuevo edo acept
        for e in self.EdosAcept:
            e._transiciones.add(Transicion(simb1=EPSILON, edo=ef))
            e.aceptacion = False

        # Actualización de IDs
        self.actualizarIds(1)
        ef.setId(self.obtenerUltimoIdEstado() + 1)
        # Se actualizan nuevos estados
        self.EdoIni = ei
        ef.aceptacion = True
        # Se actualiza AFN
        self.EdosAcept.clear()
        self.EdosAcept.add(ef)
        self.EdosAFN.add(ei)
        self.EdosAFN.add(ef)
    
    # OPCION 8 - Debe ser "Convertir AFN a AFD"

   

    # OPCION 9 - Debe ser "Analizar una cadena"

    # OPCION 10 - Debe ser "Probar analizador léxico"

    def moverA(self,edo,simb):
        
        C=set()
        aux=None

        for t in edo.getTransiciones():
            aux= t.getEdoTrans(simb)
            if aux != None:
                C.add(aux)
        
        return C
    
    def moverAEdos(self,edos,simb):
        
        C=set()
        aux=None
        for edo in edos:
            for t in edo.getTransiciones():
                aux= t.getEdoTrans(simb)
                if aux != None:
                    C.add(aux)
        
        return C
    
    def irA(self,edos,simb):
        """
        En esta parte pasamos Conjunto de estados
        Creamos Un Conjunto C que contendra a su vez Conjunto de estados
        tenemos un Conjunto de estados llamado edosAux
        iteramos sobre edosAux y sobre cada iteracion guardamos en C conjuntos de edos con los que
        se tiene la cerradura Positiva.
        """
        C=set()
        edosAux=set()
        edosAux=self.moverAEdos(edos,simb)
        # Agregué esta linea, porque cuando es igual a 1 (la mayoría de veces), no tiene caso que sea un conjunto de conjuntos
        if len(edosAux) == 1:
            for e in edosAux:
                C = frozenset(self.cerraduraEpsilon(e))
        else:
            for e in edosAux:
                C.add(frozenset(self.cerraduraEpsilon(e)))
        return C

    def cerraduraEpsilon(self,edo):
        C=set()
        pila=[]
        edoAux=None
        edoT=None
        pila.insert(0,edo)

        while pila != [] :
            bandera=0
            edoAux=pila.pop(0)
            C.add(edoAux)
            #self.imprimirTransicionesEstado(edoAux)
            for t in edoAux.getTransiciones():
                edoT = t.getEdoTransEpsilon(EPSILON)
                if edoT != None:
                    for e in C:
                        if e == edoT:
                            bandera=1   
                    if bandera <= 0:
                        pila.insert(0,edoT)
        return C

    #Esta actualizacion la hice ya que en la union se crean diversas ramas
    def actualizarIdsUnion(self):
        #Creo un conjunto de EdosAFN auxiliar
        i=1
        conjunto=set()

        """#Reasigna los Id's incrementalmente exepto si es el estado de aceptacion
           ya que en la union solo hay uno y debe de ser el id mayor 
        """
        for e in self.EdosAFN:
                if e.getAceptacion() != True:
                    e.setId(i)
                    conjunto.add(e)
                    i+=1
                else:
                    conjunto.add(e)
                
        self.EdosAFN=conjunto    

    def actualizarIds(self, n):
        """Actualiza los IDs de los estados de un AFN dado

        Args:
            n (int): Es el número al cual se incrementarán todos los IDs de los estados del AFN
        """
        # Primero se actualiza a 1,2,3,...
        i = 1
        for e in self.EdosAFN:
            e.setId(i)
            i+=1
        # Luego se actualiza con la n, que debe ser el número de estados de un AFN dado
        for e in self.EdosAFN:
            e.setId(e.idEstado + n)
    
    def obtenerUltimoIdEstado(self):
        """Obtiene el último ID que se tiene en todo el set de estados de un AFN

        Returns:
            int: ID del último estado
        """
        a = 0
        for e in self.EdosAFN:
            if e.idEstado > a:
                a = e.idEstado

        return a

    def getAlfabeto(self):
        """Regresará el alfabeto en una lista ordenada

        Returns:
            list: Lista del Alfabeto ordenada
        """
        alf = list(self.Alfabeto)
        alf.sort()
        return alf

    def getEdosAFN(self):
        return self.EdosAFN

    def limpiar(self):
        self.EdosAcept.clear()    
                
    def getEdoInicial(self):
        return self.EdoIni

    def getEdosAcept(self):
        return self.EdosAcept
    
    def setEdosAcept(self,edo): #Aniadimos al conjunto un elemento
        self.EdosAcept.add(edo)

    def setEdosAceptCompleto(self,edos): #igualamos dos conjuntos
        self.EdosAcept=edos
    
    def setEdosAFN(self,edo):
        self.EdosAFN.add(edo)

    def imprimirAFN(self):
        print("Número de estados:", len(self.EdosAFN))
        for e in self.EdosAFN:
            if e.aceptacion:
                print("Edo acept:", e)
            elif self.EdoIni == e:
                print("Edo ini:", e)
            else:
                print(e)
    
    def imprimirTransicionesEstado(self,estado):
           for t in estado.getTransiciones():
                print(estado,"-",t)

    def imprimirTransiciones(self):
        for e in self.EdosAFN:
            for t in e._transiciones:
                print(e,"-",t)

    def imprimir(self):
        print("-----\n", self)
        self.imprimirAFN()
        self.imprimirTransiciones()

# # PRUEBAS PARA CONVERSIÓN DE AFN A AFD
# # creación de (a|b)+
# a = AFN(1)
# a.crearAFNBasico('a')
# b = AFN(2)
# b.crearAFNBasico('b')
# a.unir(b)
# a.cerradurap()
# # creación de c*
# c = AFN(3)
# c.crearAFNBasico('c')
# c.cerradurak()
# # creación de (a|b)+ o c*
# a.concatenar(c)
# # a.imprimir()
# afd = AFD(a)

# # PRUEBAS PARA ANALIZADOR LÉXICO
# a = AFN()
# b = AFN()
# c = AFN()

# a.crearAFNBasico('x', 'y')
# b.crearAFNBasico('.')
# c.crearAFNBasico('0', '9')
# d = "a"

# analizador = AnalizadorLexico()
# analizador.union([a,b,c])
# print(analizador)

# # PRUEBAS PARA AFNs ([a-z] | [A-Z]) o ([a-z] | [A-Z] | [0-9])*
# # Creación de ([a-z] | [A-Z])
# a = AFN()
# a.crearAFNBasico('a', 'z')
# b = AFN()
# b.crearAFNBasico('0', '9')
# a.unir(b)
# a.imprimir()
# print("-------")
# dD=set()
# dD=a.irA(a.getEdosAFN(),'7')
# for d in dD:
#     for e in d:
#         print(e)


# # Creación de ([a-z] | [A-Z] | [0-9])*
# c = AFN()
# c.crearAFNBasico('a', 'z')
# d = AFN()
# d.crearAFNBasico('A', 'Z')
# e = AFN()
# e.crearAFNBasico('0', '9')

# c.unir(d)
# c.unir(e)
# c.imprimir()


# # PRUEBAS PARA AFNs [0-9]+, [0-9]+ o . o [0-9]+
# # Sí está bien, pero los IDs de los estados están raros xD
# c = AFN()

# a = AFN()
# a.crearAFNBasico('0', '9')
# a.cerradurap()
# print("a:", a)
# a.imprimirAFN()
# a.imprimirTransiciones()

# b = AFN()
# b.crearAFNBasico('0', '9')
# b.cerradurap()

# c.crearAFNBasico('0', '9')
# c.cerradurap()

# d = AFN()
# d.crearAFNBasico('.')

# b.concatenar(d)
# b.concatenar(c)
# print("b:", b)
# b.imprimirAFN()
# b.imprimirTransiciones()

# # PRUEBAS PARA UNIÓN
# a.crearAFNBasico('a','z')
# print("a:", a)
# b.crearAFNBasico('1','9')
# print("b:", b)
# b.UnirAFN(a)
# print("-\n-")
# b.imprimirAFN()
# print("-\n-")
# b.imprimirTransiciones()

"""
a.imprimirAFN()
a.opcional()
print("Opcional\na:", a)
a.imprimirAFN()
print("-")
a.imprimirTransiciones()
"""
# # PRUEBAS PARA CERRADURA KLEEN *
# a = AFN()
# a.crearAFNBasico('a', 'j')
# print("a:", a)
# a.imprimirAFN()
# b = AFN()
# b.crearAFNBasico('2', '3')
# a.concatenar(b)
# print("a:", a)
# a.imprimirAFN()
# a.imprimirTransiciones()
# a.cerradurak()
# print("Cerradura de Kleen\na:", a)
# a.imprimirAFN()
# a.imprimirTransiciones()

# # PRUEBAS PARA CERRADURA POSITIVA +
# a= AFN()
# a.crearAFNBasico('a', 'd')
# print("a:", a)
# a.imprimirAFN()
# a.cerradurap()
# print("a:", a)
# a.imprimirAFN()
# print("-")
# a.imprimirTransiciones()

# PRUEBAS PARA CONCATENACION
# b = AFN()
# b.crearAFNBasico('1')

# a.concatenar(b)
# print("a:", a)
# a.imprimirAFN()

# c = AFN()
# c.crearAFNBasico('g', 'k')
# a.concatenar(c)
# print("a:", a)
# a.imprimirAFN()
# print(a)
# print(b)
# a.imprimirAFN()
# b.imprimirAFN()
# a.UnirAFN(b)
# print("a:",a)
# a.imprimirAFN()

