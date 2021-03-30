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
                print("Error: No se ha creado ningún AFN porque el simbolo superior es mayor que el inferior")
                return

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
    # Acá hay errores de lógica con la numeración de Estados y la asignación del estado de aceptación
    def UnirAFN(self,f):
        e1=Estado()
        e2=Estado()

        t1=Transicion()
        t1.setEpsilon(EPSILON,self.getEdoInicial())

        e1.setTransicion(t1)
        t1.setEpsilon(EPSILON,f.getEdoInicial())
        e1.setTransicion(t1)

        for acept in self.EdosAcept:
            t1.setEpsilon(EPSILON,e2)
            acept.setAceptacion(False)
            acept.setTransicion(t1)
            self.setEdosAFN(acept)
   
        for acept in f.getEdosAcept():
            t1.setEpsilon(EPSILON,e2)
            acept.setAceptacion(False)
            acept.setTransicion(t1)
            f.setEdosAFN(acept)

        self.limpiar()
        f.limpiar()
        self.EdoIni=e1
        e2.setAceptacion(True)
        self.setEdosAcept(e2)
        self.EdosAFN=self.EdosAFN | f.getEdosAFN()
        self.setEdosAFN(e1)
        self.setEdosAFN(e2)
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
        
a= AFN()
a.crearAFNBasico('a', 'd')
print("a:", a)
a.imprimirAFN()

b = AFN()
b.crearAFNBasico('1')

a.concatenar(b)
print("a:", a)
a.imprimirAFN()

c = AFN()
c.crearAFNBasico('g', 'k')
a.concatenar(c)
print("a:", a)
a.imprimirAFN()
# print(a)
# print(b)
# a.imprimirAFN()
# b.imprimirAFN()
# a.UnirAFN(b)
# print("a:",a)
# a.imprimirAFN()
