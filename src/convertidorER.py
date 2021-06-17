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

#No eliminar por que esto es necesario para este analizador

# a = AFN()
# a.crearAFNBasico('|')
# b = AFN()
# b.crearAFNBasico('&')
# c = AFN()
# c.crearAFNBasico('+')
# d = AFN()
# d.crearAFNBasico('*')
# e = AFN()
# e.crearAFNBasico('?')
# f = AFN()
# f.crearAFNBasico('(')
# g = AFN()
# g.crearAFNBasico(')')
# h= AFN()
# h.crearAFNBasico('[')
# i = AFN()
# i.crearAFNBasico(']')
# j = AFN()
# j.crearAFNBasico('-')
# # Creación de D.D = [0-9]+ o (. o [0-9]+)?
# k = AFN()
# k.crearAFNBasico('0', '9')
# l=AFN()
# l.crearAFNBasico('a','z')
# m=AFN()
# m.crearAFNBasico('A','Z')
# n=AFN()
# n.crearAFNBasico('!')
# o=AFN()
# o.crearAFNBasico('+')
# o.opcional()
# n.concatenar(o)
# o=AFN()
# o.crearAFNBasico('*')
# o.opcional()
# n.concatenar(o)
# p=AFN()
# p.crearAFNBasico('-')
# p.opcional()
# n.concatenar(p)
# q=AFN()
# q.crearAFNBasico('.')
# q.opcional()
# n.concatenar(q)
# q=AFN()
# q.crearAFNBasico('/')
# q.opcional()
# n.concatenar(q)
# q.opcional()
# n.concatenar(q)



# # for i in range(5):
# #     o=AFN()
# #     print(chr(i))
# #     o.crearAFNBasico(chr(i))
# #     o.opcional()
# #     n.concatenar(o)
# k.unir(l)
# k.unir(m)
# k.unir(n)

# analizador = AnalizadorLexico()

# analizador.union([a,b,c,d,e,f,g,h,i,j,k])
# print(analizador.afn)
# afd = AFD(analizador.afn)

# print("Digita el nombre del AFD: ")      
# afd.exportarAFD(input())
# afdDos=AFD()
# print("Digita el nombre del AFD: ")  
# afdDos.importarAFD(input())
# #print(afdDos)
# analizador.setCadenAndTabla("[a-z]&[A-Z]&!.",afdDos)#2.8+7*4
# analizador.analizarCadena()
# # con=convertidorER(analizador)
# # con.IniConversion()
# # afnR=con.getResultado()
# # print("\n")
# # afnR.imprimir()
# # #con=convertidorPostfijo(analizador)
# # con.ConvPostfijo()

# # print(con.getCadenaPost())  
