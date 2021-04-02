from Estado import *
from Transicion import *

# Simulación clase SimbolosEspeciales
EPSILON = chr(5)
FIN = chr(0)

class AFN():
    def __init__(self):
        self.incremento=0
        self.EdoIni=None
        self.EdosAcept=set()
        self.EdosAFN=set()
        self.Alfabeto = []
        self.idAFN=0
    
    # OPCIÓN 1
    # AFNBasico para simbolo inferior (o superior)
    def crearAFNBasico(self,simbolo, s2=None):
        """Crea un AFN básico a partir de 1 o 2 símbolos

        Args:
            simbolo (chr): El caracter (inferior) principal que irá en el AFN
            s2 (chr, optional): El caracter superior. Defaults to None.
        """
        # Se valida primero s2
        simbolo2 = simbolo
        # Esto simula la sobreescritura del método
        if s2 != None:
            if ord(simbolo) < ord(s2):
                # Si todo es valido entonces
                simbolo2 = s2
            else:
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
        for i in range(ord(simbolo), ord(simbolo2) + 1):
            # self.Alfabeto.add(chr(i))
            self.Alfabeto.append(chr(i))

        self.EdoIni=e1
        self.setEdosAFN(e1)
        self.setEdosAFN(e2)
        self.setEdosAcept(e2)
        # self.setAlfabeto(simbolo)

    # OPCIÓN 2
    def UnirAFN(self,f):
        #Creamos dos conjuntos auxiliares para los EdosAFN
        conjuntoA=set()
        conjuntoB=set()
        #Llenamos los conjuntos auxiliares
        for c in self.EdosAFN:
            if c.getAceptacion() != True:
                conjuntoA.add(c)

        for c in f.getEdosAFN():
            if c.getAceptacion() != True :
                conjuntoB.add(c)

        #Creamos Estados inicial=1 y final=2 junto con las transiciones
        e1=Estado()
        e2=Estado()
        t1=Transicion()
        t2=Transicion()
        t1.setEpsilon(EPSILON,self.getEdoInicial())
        t2.setEpsilon(EPSILON,f.getEdoInicial())
        e1.setTransicion(t1)
        e1.setTransicion(t2)

        """Aniadimos la transicion EPSILON a los conjuntos de aceptacion y
           eliminamos la aceptacion,aniadiendo asi anuestros Estados a los conjuntos aux 
        """
        for acept in self.EdosAcept:
            t1.setEpsilon(EPSILON,e2)
            acept.setAceptacion(False)
            acept.setTransicion(t1)
            conjuntoA.add(acept)
   
        for acept in f.getEdosAcept():
            t1.setEpsilon(EPSILON,e2)
            acept.setAceptacion(False)
            acept.setTransicion(t1)
            conjuntoB.add(acept)

        #Limpiamos los estados de aceptacion tanto de self como de f
        self.limpiar()
        f.getEdosAcept().clear()

        #e1 se hace el estado inicial y e2 Estado de aceptacion
        self.EdoIni=e1
        e1.setId(1)
        e2.setAceptacion(True)
        
        #Unimos Nuestros conjuntos auxiliares y añadimos nuestros estados e1 y e2 a EstadosAFN
        self.EdosAFN= conjuntoA | conjuntoB
        e2.setId(len(self.EdosAFN)+2)
        self.setEdosAFN(e1)
        self.setEdosAFN(e2)

        #Actualizamos los alfabetos y actualizamos los Id's
        self.actualizarIdsUnion()
        self.setEdosAcept(e2)
        self.Alfabeto = self.Alfabeto + f.getAlfabeto()
        
        return self
    
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
        self.Alfabeto += f.Alfabeto

    # OPCIÓN 4
    def cerradurap(self):
        """Cerradura positiva de un AFN
        """
        # Se crea un nuevo edo inicial y final de aceptación
        ei = Estado()
        ef = Estado()

        # Se crean y añaden las transiciones epsilon
        ei._transiciones.add(Transicion(simb1=EPSILON, edo=ei))
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

    def __str__(self):
        return "El alfabeto es:"+ str(self.Alfabeto)

    def getAlfabeto(self):
        return self.Alfabeto

    def getEdosAFN(self):
        return self.EdosAFN

    def limpiar(self):
        self.EdosAcept.clear()    
                
    def getEdoInicial(self):
        return self.EdoIni

    def getEdosAcept(self):
        return self.EdosAcept

    # def setAlfabeto(self,simbolo):
    #     self.Alfabeto.add(simbolo)
    
    def setEdosAcept(self,edo): #Aniadimos al conjunto un elemento
        self.EdosAcept.add(edo)

    def setEdosAceptCompleto(self,edos): #igualamos dos conjuntos
        self.EdosAcept=edos
    
    def setEdosAFN(self,edo):
        self.EdosAFN.add(edo)

    def imprimirAFN(self):
        for e in self.EdosAFN:
            if e.aceptacion:
                print("Edo acept:", e)
            else:
                print(e)

    def imprimirTransiciones(self):
        for e in self.EdosAFN:
            for t in e._transiciones:
                print(t)

# PRUEBAS PARA OPCIONAL ?
a = AFN()
b= AFN()
c= AFN()

a.crearAFNBasico('a','z')
print("a:", a)
b.crearAFNBasico('1','9')
print("b:", b)
c.crearAFNBasico('A','Z')
print("c",c)

b.UnirAFN(a)
c.UnirAFN(b)
c.imprimirAFN()

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

