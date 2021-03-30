from Transicion import *

class Estado(object):
    """Representa un estado junto con las transiciones que tiene y si es de aceptación o no
    """
    def __init__(self):
        self.idEstado=1
        self.transiciones=set()
        self.aceptacion=False
        self.token=-1

    def setId(self,id):
        self.idEstado=id

    def setAceptacion(self,acept):
        self.aceptacion=acept
        
    def setTransicion(self,trans):
        self.transiciones.add(trans)
    
    def __str__(self):
        return "e" + str(self.idEstado)

    # A partir de aqui agregué a la clase pythonic getters & setters
    # @property
    # def transiciones(self):
    #     """Getter de transiciones"""
    #     return self.transiciones
    # # @transiciones.setter
    # def transiciones(self, value):
    #     """Setter de transiciones"""
    #     self.transiciones = value
    