from AFD import *


class AnalizadorLexico(object):
    """
        Representa un analizador léxico que se construye a partir de AFNs
    """
    def __init__(self, archivo = None):
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
        self._archivo = archivo
        if archivo != None:
            self.importar(archivo)
   
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
    @property
    def archivo(self):
    
        """El nombre del archivo de donde se obtuvo la tabla AFD

        Returns:
            str: Nombre del archivo
        """
        return self._archivo
    @archivo.setter
    def archivo(self, value):
        self._archivo = value

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

    def setCadena(self,cadena):
        self.CadenaSigma=cadena
        
    def setCadenAndTabla(self,cadena,afd):
        self.CadenaSigma=cadena
        self.tablaAFD=afd.getTablaAFD()

    def yylex(self,lexemab=None):
        lexban=0
        if lexemab!=None:
            lexban=1
        banderaCaracter=0
        j=0
        numTrans=0
        tam=0
        self.pila.insert(0,self.IndiceCaracterActual)
        #print(self.tablaAFD)
        if self.IndiceCaracterActual >= len(self.CadenaSigma):
           self.Lexema=""
           if lexban==0:        
             return EPSILON
           elif lexban==1:
             return EPSILON,self.Lexema 
        
        self.Inilexema=self.IndiceCaracterActual
        self.EdoActual = 0
        self.PasoPorEdoAcept=False
        self.finLexema=-1
        self.token="-1"
        i=self.IndiceCaracterActual
        # Solución *temporal* para poder leer espacios
        if len(self.tablaAFD[0]) < len(self.tablaAFD[1]):
            self.tablaAFD[0].insert(1, ' ')

        for t in self.tablaAFD:
            tam=len(t)
        
        while i < len(self.CadenaSigma):
            #print("Dist",self.finLexema,self.IndiceCaracterActual)
            self.caracterActual=self.CadenaSigma[self.IndiceCaracterActual]
            #print(self.caracterActual)
            #print(self.caracterActual) 
            banderaCaracter=0

            while j < tam : #len(self.tablaAFD[0])
                if self.caracterActual==self.tablaAFD[0][j]:
                    banderaCaracter=1
                    etr = self.EdoTransicion
                    self.EdoTransicion=int(self.tablaAFD[self.EdoActual+1][j])
                    # SOLUCIÓN TEMPORAL para que "self.tablaAFD[self.EdoTransicion+1]" no se desborde
                    self.EdoTransicion = etr if self.EdoTransicion > len(self.tablaAFD) else self.EdoTransicion
                 
                j+=1
            if banderaCaracter==0:
                i=len(self.CadenaSigma)+1
            j=0

            if self.EdoTransicion != -1 and self.EdoTransicion != None and banderaCaracter!=0:
                # print(self.EdoTransicion, tam)
                if self.tablaAFD[self.EdoTransicion+1][tam-1]!='-1': #self.tablaAFD[self.EdoActual])
                   self.PasoPorEdoAcept=True
                   self.token=self.tablaAFD[self.EdoTransicion+1][tam-1]
                   self.finLexema=self.IndiceCaracterActual
                   

                self.IndiceCaracterActual+=1
                i+=1
                self.EdoActual=self.EdoTransicion
            else:
                i=len(self.CadenaSigma)+1
            
        if self.PasoPorEdoAcept is False and banderaCaracter==0:
            self.IndiceCaracterActual=self.Inilexema+1
            self.Lexema=self.CadenaSigma[self.Inilexema]
            self.token="ERROR"
        #print("p",self.Lexema,self.Inilexema,self.finLexema,self.IndiceCaracterActual)
        if self.Inilexema!=self.finLexema and banderaCaracter!=0:
            self.Lexema=self.CadenaSigma[self.Inilexema:self.finLexema+1]
        else:
            if banderaCaracter!=0:
                self.Lexema=self.CadenaSigma[self.Inilexema] 
        #print(self.Lexema,self.Inilexema,self.finLexema,self.IndiceCaracterActual)
        if banderaCaracter!=0 :
            self.IndiceCaracterActual=self.finLexema+1
        
        if self.PasoPorEdoAcept is True and banderaCaracter==0:
            if self.Inilexema!=self.finLexema:
                self.Lexema=self.CadenaSigma[self.Inilexema:self.finLexema+1]
            else:
                self.Lexema=self.CadenaSigma[self.Inilexema]
        if lexban==0:        
            return self.token
        elif lexban==1:
            return self.token,self.Lexema

    def analizarCadena(self):
        tokenlocal=""
        while self.IndiceCaracterActual<len(self.CadenaSigma):
            tokenlocal=self.yylex()
            # Solución (temporal) para que no se cicle el programa
            if tokenlocal == '-1' or tokenlocal == 'ERROR':
                if self.IndiceCaracterActual < len(self.CadenaSigma):
                    self.Lexema = self.CadenaSigma[self.IndiceCaracterActual]
                tokenlocal = "ERROR"
                self.IndiceCaracterActual += 1
            strlex = "'" + str(self.Lexema) + "'"
            print("Token:",tokenlocal, "| Lexema:", strlex)

        self.resetattributes()

    def importar(self, file):
        """Importa y guarda el nombre de un archivo que contiene un AFD

        Args:
            file (str): El nombre del archivo
        """
        a = AFD()
        a.importarAFD(file)
        self.tablaAFD = a.tabla

    def resetattributes(self):
        """Resetea los atributos utilizados para el análisis de una cadena en la función yylex
        """
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

    def undotoken(self):
        if len(self.pila) == 0:
            return False
        self.IndiceCaracterActual = self.pila.pop(0)
        return True

    def getparams(self):
        """Obtiene todos los parámetros que hacen funcionar al analizador léxico

        Returns:
            list: Los parámetros en una lista
        """
        return self.Inilexema, self.EdoActual, self.PasoPorEdoAcept, self.finLexema, self.token, self.pila, self.Lexema, self.IndiceCaracterActual, self.caracterActual, self.EdoTransicion

    def setparams(self, params:list):
        """Establece parametros que del analizador léxico

        Args:
            params (list): La lista de parámetros
        """
        self.Inilexema              = params[0]
        self.EdoActual              = params[1]
        self.PasoPorEdoAcept        = params[2]
        self.finLexema              = params[3]
        self.token                  = params[4]
        self.pila                   = params[5]
        self.Lexema                 = params[6]
        self.IndiceCaracterActual   = params[7]
        self.caracterActual         = params[8]
        self.EdoTransicion          = params[9]