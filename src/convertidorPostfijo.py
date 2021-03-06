from evaluadorcalc import *

class convertidorPostfijo(object):

    def __init__(self,analizador: AnalizadorLexico):
        self._anLexico=analizador
        self._lexPos=""


    def ConvPostfijo(self):
        v=""
        ref=[v]
        if (self.E(ref)):
            if (self._anLexico.yylex() == EPSILON):
                self._lexPos =ref[0]
                return True
        return False

    def E(self,v):
        if self.T(v):
            if self.Ep(v):
                return True
        return False
    
    def Ep(self,v):
        token=self._anLexico.yylex()
        v2=""
        ref=[v2]
        
        if token=="10" or token =="20":
            if self.T(ref):
                v[0]=v[0]+" "+ref[0]+" "
                if token == "10":
                    v[0]+="+"
                elif token == "20":
                    v[0]+="-"
                if self.Ep(v):
                    return True
            return False
        self._anLexico.undotoken()
        return True

    def T(self,v):
        if self.F(v):
            if self.Tp(v):
                return True
        return False
    
    def Tp(self,v):
        token=self._anLexico.yylex()
        v2=""
        ref=[v2]
        if token =="30" or token =="40":
            if self.F(ref):
                v[0]=v[0]+" "+ref[0]+" "
                if token == "30":
                    v[0]+="*"
                elif token == "40":
                    v[0]+="/"
                if self.Tp(v):
                    return True
            return False
        self._anLexico.undotoken()
        return True
    
    def F(self,v):
        token=self._anLexico.yylex()
        if token == "50":
            if self.E(v):
                token=self._anLexico.yylex()
                if token == "60":

                    return True
            return False
        elif self.if_integer(token):
            #print(self._anLexico.Lexema+"\n")
            v[0]=self._anLexico.Lexema #self._anLexico.Lexema()
            return True
        else:
            return False
    
    def detectaNum(self,v):
        if v[0]== "0" or v[0]== "1" or v[0]== "2" or v[0]== "3" or v[0]== "4" or v[0]== "5" or v[0]== "6" or v[0]== "7" or v[0]== "8" or v[0]== "9":
            return True
        else:
            return False

    def if_integer(self,string):
  
        if string[0] == '-':
            return False

        else:
            return string.isdigit()

    def getCadenaPost(self):
        return self._lexPos
