from convertidorPostfijo import *

class convertidorER(object):

    def __init__(self,analizador: AnalizadorLexico):
        self._anLexico=analizador
        self._expRegular=""
        self._result=None
    
    def IniConversion(self):
        f=AFN()
        #ref=[f]
        if self.E(f):
            if self._anLexico.yylex() == EPSILON:
                self._result =f
                return True
        return False

    def E(self,f):
        if self.T(f):
            if self.Ep(f):
                return True
        return False
    
    def Ep(self,f):
        #f.imprimir()
        f2=AFN()
        
        #result2=[f2]
        token=self._anLexico.yylex()
        if token=="10": #OR
            if self.T(f2):
                f.unir(f2)
                if self.Ep(f):
                    return True
            return False
        self._anLexico.undotoken()
        return True
        
    def T(self,f):
        if self.C(f):
            if self.Tp(f):
                return True
        return False

    def Tp(self,f):
        f2=AFN()
        #result2=[f2]
        token=self._anLexico.yylex()
        if token=="20": #Concatenacion
            if self.T(f2):
                f.concatenar(f2)
                if self.Tp(f):
                    return True
            return False
        self._anLexico.undotoken()
        return True  

    def C(self,f):
        if self.F(f):
            if self.Cp(f):
                return True
        return False  
    
    def Cp(self,f):
        token=self._anLexico.yylex()
        if token=="30": #Transitiva
            f.cerradurap()
            if self.Cp(f):
                return True
            return False
        elif token=="40": #Klean
            f.cerradurak()
            if self.Cp(f):
                return True
            return False
        elif token=="50": #Opcional
            f.opcional()
            if self.Cp(f):
                return True
            return False
        self._anLexico.undotoken()
        return True
    
    def F(self,f):
        token=self._anLexico.yylex()
        s1=""
        s2=""

        if token=="60": # Parentesis (
            if self.E(f):
               token=self._anLexico.yylex()
               if token=="70":  # Parentesis )
                   return True
            return False
        elif token=="80": # Corchete [
            token=self._anLexico.yylex()
            if token=="110": #Simbolo
                if self._anLexico.Lexema[0:1]=="!":
                    s1=self._anLexico.Lexema[1:2]
                else:
                    s1=self._anLexico.Lexema[0:1]
                token=self._anLexico.yylex()
                if token== "100":#Guion
                    token=self._anLexico.yylex()
                    if token=="110": #Simbolo2
                        if self._anLexico.Lexema[0:1]=="!":
                            s2=self._anLexico.Lexema[1:2]
                        else:
                            s2=self._anLexico.Lexema[0:1]
                        token=self._anLexico.yylex()    
                        if token=="90": #Corchete ]
                            #f=AFN()
                            f.crearAFNBasico(s1,s2)
                            return True
            return False
        elif token=="110": #SIMB
              if self._anLexico.Lexema[0:1]=="!":
                    s1=self._anLexico.Lexema[1:2]
              else:
                    s1=self._anLexico.Lexema[0:1]
              #f=AFN()
              f.crearAFNBasico(s1)
              return True
        return False
    def getResultado(self):
        return self._result
        