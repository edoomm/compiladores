# Clase responsable de analizar una expresión matemática y evaluarla

from AnalizadorLexico import *

class Evaluador(object):
    def __init__(self, anlex: AnalizadorLexico):
        self._anlex = anlex
        self._result = None

    ''' Atributos
    '''
    @property
    def anlex(self):
        """El analizador léxico que contendrá la tabla AFD

        Returns:
            AnalizadorLexico: El objeto asociado a este atributo
        """
        return self._anlex
    @anlex.setter
    def anlex(self, value):
        self._anlex = value
    @property
    def result(self):
        return self._result
    @result.setter
    def result(self, value):
        self._result = value
    
    ''' Métodos
    '''
    def inieval(self):
        v = float("0")
        ref = [v]
        if (self.E(ref)):
            if (self.anlex.yylex() == EPSILON):
                self.result = v
                return True
        return False

    def E(self, v):
        if (self.T(v)):
            if (self.Ep(v)):
                return True
        return False

    def Ep(self, v):
        v2 = float(0)
        token = self.anlex.yylex()
        # + ó -
        if token == 10 or token == 20:
            ref = [v2]
            if (self.T(ref)):
                v[0] = v[0] + (ref[0] if token == 10 else -ref[0])
                if (self.Ep(v)):
                    return True
            return False
        self.anlex.undotoken()
        return True

    def T(self, v):
        if self.F(v):
            if (self.Tp(v)):
                return True
        return False

    def Tp(self, v):
        v2 = float(0)
        token = self.anlex.yylex()
        if token == 40 or token == 50:
            ref = [v2]
            if self.F(ref):
                v[0] = v[0] * (ref[0] if token == 30 else 1/ref[0])
                if self.Tp(v):
                    return True
            return False
        self.anlex.undotoken()
        return True

    def F(self, v):
        token = self.anlex.yylex()
        if token == 50:
            if (self.E(v)):
                token = self.anlex.yylex()
                if token == 70:
                    return True
            return False
        elif token == 10:
            v[0] = float(self.anlex.lexema)
            return True
        
        return False

