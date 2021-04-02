

class Transicion():
    """Representa la transicion que se hace de un estado a otro estado a través de uno o más símbolos
        
    Args:
        simb1 (str, optional): Símbolo inferior de un rango dado de símbolos. Defaults to ''.
        simb2 (str, optional): Símbolo superior de un rango dado de símbolos. Defaults to ''.
        edo (Estado, optional): Estado al que se llegará a través de estos símbolos. Defaults to None.
    """
    def __init__(self, simb1 = '', simb2 = '', edo = None): 
        # Se simula el overload de un solo símbolo, para que SInferior = SSuperior
        if simb1 != '' and simb2 == '':
            simb2 = simb1

        self.SInferior = simb1
        self.SSuperior = simb2
        self.estado = edo
     

    def setParametros(self,Inf,Sup,e):
        self.SInferior=Inf   
        self.SSuperior=Sup
        self.estado=e

    def setEpsilon(self,simb,e):
        self.SInferior=simb  
        self.SSuperior=simb
        self.estado=e

    def __str__(self):
        return str(self.estado) + " " + self.SInferior + "-" + self.SSuperior