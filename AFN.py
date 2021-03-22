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
        self.Alfabeto=set()
        self.idAFN=0
    
    def crearAFNBasico(self,simbolo):
        self.incremento+=1
        e1=Estado()
        e1.setId(self.incremento)
        e2=Estado()
        self.incremento+=1
        e2.setId(self.incremento)
        t=Transicion()
        t.setParametros(e1,e2,simbolo)
        e2.setAceptacion(True)
        e1.setTransicion(t)
        self.EdoIni=e1
        self.setEdosAFN(e1)
        self.setEdosAFN(e2)
        self.setEdosAcept(e2)
        self.setAlfabeto(simbolo)

    def UnirAFN(self,f):
        e1=Estado()
        e2=Estado()
        t1=Transicion()
        t1.setParametros(e1,self.getEdoInicial(),EPSILON)
        e1.setTransicion(t1)
        t1.setParametros(e1,f.getEdoInicial(),EPSILON)
        e1.setTransicion(t1)
        for acept in self.EdosAcept:
            t1.setParametros(acept,e2,EPSILON)
            e2.setTransicion(t1)

        for acept in f.getEdosAcept():
            t1.setParametros(acept,e2,EPSILON)
            e2.setTransicion(t1)

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

    def setAlfabeto(self,simbolo):
        self.Alfabeto.add(simbolo)
    
    def setEdosAcept(self,edo):
        self.EdosAcept.add(edo)
    
    def setEdosAFN(self,edo):
        self.EdosAFN.add(edo)

    def imprimirAFN(self):
        for e in self.EdosAFN:
            print(e)
                
                

    
        
a= AFN()
a.crearAFNBasico('a')
a.crearAFNBasico('b')
print(a)
a.imprimirAFN()
