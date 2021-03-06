from convertidorER import *

class GramaticasDeGramaticas(object):
    def __init__(self,analizador: AnalizadorLexico):
        self._anLexico      = analizador
        self._result        = None
        self._ListaReglas   = []
        self._ListaFila     = []
        self._auxIzq        = ""
        self._aux           = ""
    
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
    ### Sintacticos
    def getToken(self):
        """Obtiene el token del analizador léxico descartando los espacios
        """
        token,self._aux= self.anlex.yylex(1)
        #print("-"+self._aux+"\n")

        if token !="40":
            return token
        else:
            token,self._aux=self.anlex.yylex(1)
        return token

    def inieval(self):
        if self.G():
            if self.getToken() == EPSILON:
                return True
        return False
    
    def G(self):
        if self.ListaReglas():
            return True
        return False
    
    def ListaReglas(self):
        if self.Regla():
            if self.getToken() == "10": # PUNTO Y COMA
                if self.ListasReglasP():
                    return True
        return False

    def ListasReglasP(self):
        p = self.anlex.getparams()
        if self.Regla():
            if self.getToken() == "10": # PUNTO Y COMA
                if self.ListasReglasP():
                    return True
            return False
        self.anlex.setparams(p)
        return True
    
    def Regla(self):
        self._ListaFila=[]
        if self.LadoIzq():
            self._ListaFila.append(self._auxIzq)
            if self.getToken() == "20": # FLECHA
                if self.LadosDerechos():
                    return True
        return False

    def LadoIzq(self):
        if self.getToken() == "30": # SIMBOLO
            self._auxIzq=self._aux #Guardamos lado Izquierdo
            return True
        return False

    def LadosDerechos(self):
        if self.LadoDerecho():
            self._ListaReglas.append(self._ListaFila)
            self._ListaFila=[]
            self._ListaFila.append(self._auxIzq)
            if self.LadosDerechosP():
                return True
        return False

    def LadosDerechosP(self):
        if self.getToken() == "50": # OR
            if self.LadoDerecho():
                self._ListaReglas.append(self._ListaFila)
                self._ListaFila=[]
                self._ListaFila.append(self._auxIzq)
                if self.LadosDerechosP():
                    return True
            return False
        self.anlex.undotoken()
        return True

    def LadoDerecho(self):
        if self.getToken() == "30": # SIMBOLO
            self._ListaFila.append(self._aux) #Agregando Simbolo lado derecho
            if self.LadoDerechoP():
                return True
        return False

    def LadoDerechoP(self):
        if self.getToken() == "30": # SIMBOLO
            self._ListaFila.append(self._aux) #Agregando Simbolo lado derecho
            if self.LadoDerechoP():
                return True
            return False
        self.anlex.undotoken()
        return True

    ### Otros
    def imprimirListaReglas(self):
        for l in self._ListaReglas:
            print('|', l[0], '|', sep='', end='->')
            for lf in l[1:len(l)]:
                print(lf, end='->')
            print("‖", end="\n----\n")
