from AFN import *

class AnalizadorLexico(object):
    """
        Representa un analizador léxico que se construye a partir de AFNs
    """
    def __init__(self):
        self._afn = AFN()
        self.CadenaSigma=None #cadena
        self.tablaAFD=None#tablaAFD
        self._tokens = []
        self.Inilexema=0
        self.EdoActual=0
        self.PasoPorEdoAcept=False
        self.finLexema=0
        self.token=0
        self.pila=[]
        self.Lexema=""
        self.IndiceCaracterActual=0
        self.caracterActual=""
        self.EdoTransicion=0
   
    def __str__(self):
        self.afn.imprimir()
        strtokens = "Tokens: "
        for t in self.tokens:
            strtokens += "(" + str(t[0]) + ", " + str(t[1]) + "), "
        return strtokens[:len(strtokens)-2]

    ''' Atributos
    '''
    @property
    def tokens(self):
        return self._tokens
    @tokens.setter
    def tokens(self, value):
        self._tokens = value
    @property
    def afn(self):
        return self._afn
    @afn.setter
    def afn(self, value):
        self._afn = value
    
    def setCadenAndTabla(self,cadena,afd):
        self.CadenaSigma=cadena
        self.tablaAFD=afd.getTablaAFD()

    ''' Métodos
    '''
    # OPCION 7 - Debe ser "Unión para Analizador Léxico"
    def union(self, afns):
        """Une una lista de AFNs en un AFN Especial que es el analizador léxico

        Args:
            afns (list): Lista de los AFNs a unir
        """
        # Se validan que sean AFNs primero
        for a in afns:
            if not isinstance(a, AFN):
                print("El objeto", a, "no es un AFN")
                return None

        # Se crea el estado inicial y se añaden las transiciones epsilon a los AFNs
        ei = Estado()
        ei.setId(0)
        ultimoId = 0
        token = 10
        # Atributos del AFN Especial
        edosacc = set()
        edosafn = set()
        alf = set()
        # Recorrido por todo
        for a in afns:
            ei._transiciones.add(Transicion(simb1=EPSILON, edo=a.EdoIni))
            a.actualizarIds(ultimoId)
            ultimoId = a.obtenerUltimoIdEstado()
            alf = alf | a.Alfabeto
            # Añadiendo estados de aceptación
            for eacc in a.getEdosAcept():
                edosacc.add(eacc)
                eacc.token = token
                self.tokens.append((eacc, token))
            token += 10
            # Añadiendo estados
            for edo in a.getEdosAFN():
                edosafn.add(edo)
        
        # Asociando atributos al AFN Especial
        self.afn.EdoIni = ei
        self.afn.EdosAcept = edosacc
        self.afn.EdosAFN = edosafn
        self.afn.EdosAFN.add(ei)
        self.afn.Alfabeto = alf

    
    def yylex(self):
        banderaCaracter=0
        j=0
        numTrans=0
        tam=0
        self.pila.insert(0,self.IndiceCaracterActual)
        #print(self.tablaAFD)
        if self.IndiceCaracterActual >= len(self.CadenaSigma):
           self.Lexema=""
           return EPSILON
        
        self.Inilexema=self.IndiceCaracterActual
        self.EdoActual = 0
        self.PasoPorEdoAcept=False
        self.finLexema=-1
        self.token="-1"
        i=self.IndiceCaracterActual

        for t in self.tablaAFD:
            tam=len(t)
            
        while i < len(self.CadenaSigma):
            # print("Indice Caracter Actual:", self.IndiceCaracterActual, "; Lexema:", self.Lexema, "; IniLexema:", self.Inilexema, "; FinLexema: ", self.finLexema, "; CadenaSigma: ", self.CadenaSigma)
            #print("Dist",self.finLexema,self.IndiceCaracterActual)
            self.caracterActual=self.CadenaSigma[self.IndiceCaracterActual]
            #print(self.caracterActual)
            #print(self.caracterActual) 
            banderaCaracter=0

            while j < tam : #len(self.tablaAFD[0])
                if self.caracterActual==self.tablaAFD[0][j]:
                    banderaCaracter=1
                    self.EdoTransicion=int(self.tablaAFD[self.EdoActual+1][j])
                    #print(self.EdoTransicion)
                j+=1
            j=0

            if self.EdoTransicion != -1 and self.EdoTransicion != None:
                if self.tablaAFD[self.EdoTransicion+1][tam-1]!='-1': #self.tablaAFD[self.EdoActual])
                   self.PasoPorEdoAcept=True
                   self.token=self.tablaAFD[self.EdoTransicion+1][tam-1]
                   self.finLexema=self.IndiceCaracterActual
                self.IndiceCaracterActual+=1
                i+=1
                self.EdoActual=self.EdoTransicion
            else:
                i=len(self.CadenaSigma)
            
        if self.PasoPorEdoAcept is False or banderaCaracter==0:
            self.IndiceCaracterActual=self.Inilexema+1
            self.Lexema=self.CadenaSigma[self.Inilexema:1]
            self.token="ERROR"
       
        if self.Inilexema!=self.finLexema:
            self.Lexema = self.CadenaSigma[self.Inilexema:self.finLexema+1]
        else:
            # print("2!")
            self.Lexema=self.CadenaSigma[self.Inilexema] 
        #print(self.Lexema,self.Inilexema,self.finLexema,self.IndiceCaracterActual)
        self.IndiceCaracterActual=self.finLexema+1
        return self.token

    def analizarCadena(self):
        while self.IndiceCaracterActual<len(self.CadenaSigma):
            self.yylex()
            print("\n",self.Lexema," Token:",self.token)
 