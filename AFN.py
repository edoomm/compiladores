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
        self.Alfabeto=self.Alfabeto | f.getAlfabeto()
        
        return self
    
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
            print(e)
        
a= AFN()
a.crearAFNBasico('a', 'd')
# b = AFN()
# b.crearAFNBasico('z')
print(a)
# print(b)
a.imprimirAFN()
# b.imprimirAFN()
