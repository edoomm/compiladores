
from Transicion import *

class Estado():

    def __init__(self):
        self.idEstado=1
        self.transiciones=set()
        self.aceptacion=False

    def setId(self,id):
        self.idEstado=id

    def setAceptacion(self,acept):
        self.aceptacion=acept
    
    def setTransicion(self,trans):
        self.transiciones.add(trans)
    
    def __str__(self):
        return "e" + str(self.idEstado)
    