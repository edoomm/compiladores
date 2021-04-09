from Transicion import *

class Estado(object):
    """Representa un estado junto con las transiciones que tiene y si es de aceptación o no
    """
    def __init__(self):
        self.punto=0   #este nuevo valor nos servira para saber si es el primero o el ultimo estado 0=intermedio 1=primero 2=ultimo
        self.idEstado=1
        self._transiciones=set()
        self._aceptacion=False
        self.token=-1
    
    def setPunto(self,num):
        self.punto=num
    
    def getPunto(self):
        return self.punto

    def setId(self,id):
        self.idEstado=id

    def setAceptacion(self,acept):
        self._aceptacion=acept

    def getAceptacion(self):
        return self._aceptacion

    def getTransiciones(self):
        return self._transiciones
        
    def setTransicion(self,trans):
        self._transiciones.add(trans)
    
    def __str__(self):
        return "e" + str(self.idEstado)

    # A partir de aqui agregué a la clase pythonic getters & setters
    @property
    def aceptacion(self):
        return self._aceptacion

    @aceptacion.setter
    def aceptacion(self, value):
        self._aceptacion = value

    