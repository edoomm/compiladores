

class Transicion():

    def __init__(self): 
        self.SInferior=''   
        self.SSuperior=''
        self.estado=None

    def setParametros(self,Inf,Sup,e):
        self.SInferior=Inf   
        self.SSuperior=Sup
        self.estado=e

    def setEpsilon(self,simb,e):
        self.SInferior=simb  
        self.SSuperior=simb
        self.estado=e