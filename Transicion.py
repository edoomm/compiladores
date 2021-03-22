

class Transicion():

    def __init__(self): 
        self.eInferior=None   #Estas dos variables nos marcaran el Estado Superior e Inferior
        self.eSuperior=None
        self.simbolo=''

    def setParametros(self,Inf,Sup,simb):
        self.eInferior=Inf   #Estas dos variables nos marcaran el Estado Superior e Inferior
        self.eSuperior=Sup
        self.simbolo=simb