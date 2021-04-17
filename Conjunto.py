from Transicion import *
"""
    Esta clase van a ser los Estados del AFD
"""
class Conjunto():
    
    

    def crearConjunto(self,conjunto):
        self.transicion=Transicion()
        self.conjuntoEstados=conjunto
        self.banderacheck=1

    def getConjunto(self):
        return self.conjuntoEstados

    def getbanderaCheck(self):
        return self.banderacheck

    def setConjuntos(self,conjunto):
        self.conjuntoEstados=conjunto

    def setbanderacheck(self, banderacheck):
        self.banderacheck=banderacheck
    
    