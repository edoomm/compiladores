from convertidorER import *

class GramaticasDeGramaticas(object):
    def __init__(self,analizador: AnalizadorLexico):
        self._anLexico  = analizador
        self._result    = None
    
    ''' Atributos
    '''
    @property
    def anlex(self):
        """El analizador léxico que contendrá la tabla AFD

        Returns:
            AnalizadorLexico: El objeto asociado a este atributo
        """
        return self._anLexico
    @anlex.setter
    def anlex(self, value):
        self._anLexico = value
    @property
    def result(self):
        return self._result
    @result.setter
    def result(self, value):
        self._result = value
    
    ''' Métodos
    '''
    def ini(self):
        if self.G():
            if self.anlex.yylex() == EPSILON:
                return True
        return False
    
    def G(self):
        if self.Regla():
            if self.anlex.yylex() == 10: # PUNTO Y COMA
                if self.ListaReglasP():
                    return True
        return False

    def ListasReglasP(self):
        if self.Regla():
            if self.anlex.yylex() == 10: # PUNTO Y COMA
                if self.ListaReglasP():
                    return True
            return False
        self.anlex.undotoken()
        return True
    
    def Regla(self):
        if self.LadoIzq():
            if self.anlex.yylex() == 20: # FLECHA
                if self.LadosDerechos():
                    return True
        return False

    def LadoIzq(self):
        if self.anlex.yylex() == 30: # SIMBOLO
            return True
        return False

    def LadosDerechos(self):
        if self.LadoDerecho():
            if self.LadosDerechosP():
                return True
        return False

    def LadosDerechosP(self):
        if self.anlex.yylex() == 50: # OR
            if self.LadoDerecho():
                if self.LadosDerechosP():
                    return True
            return False
        self.anlex.undotoken()
        return True

    def LadoDerecho(self):
        if self.anlex.yylex() == 30: # SIMBOLO
            if self.LadoDerechoP():
                return True
        return False

    def LadoDerechoP(self):
        if self.anlex.yylex() == 30: # SIMBOLO
            if self.LadoDerechoP():
                return True
            return False
        self.anlex.undotoken()
        return True

#################################################################################################
#   TEST SECTION                                                                                #
#################################################################################################

analizador = AnalizadorLexico("grams")
op = 2
analizador.CadenaSigma = input("Cadena a analizar: ") if op == 1 else "E->E MAS T|E MENOS T|T;T->T POR F|T ENTRE F|F;F->P_I E P_D|NUM;"
gx2 = GramaticasDeGramaticas(analizador)
print("CORRECTO" if gx2.ini() else "INCORRECTO")