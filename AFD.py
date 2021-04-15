from AFN import *
from Conjunto import * 
class AFD(): 
 
    def __init__(self,automataAFN):
        self.EstadosConjunto=Conjunto()
        self.EstadosConjunto.crearConjunto(automataAFN.cerraduraEpsilon(automataAFN.getEdoInicial()))
        self.automataAFN=automataAFN 
    
    def transformarAFNtoAFD(self,Ssuper):
        #pasamos un conjunto de estados AFD los estados son objetos de la clase Conjunto
        Ss=Ssuper 
        EstadosConjuntoAux=Conjunto() #Este objeto no se quedara , se necesita ser dinamico
        Saux=set()  #Creamos un conjunto auxiliar
        Saux=Ss #Lo igualamos al primero
        IraEstados=set() #Para guardar los conjuntos de estados  Ira 
        """
            En esta parte lo que se pretende es ir recorriendo mi conjunto de estados asta poder hacer la connecion mediante
            trancicion a la letra de cada estados y asi poder dormar mis estados Sn

        """
        for s in Ss:
            if s.getbanderaCheck()==1:
                for caracter in self.automataAFN.getAlfabeto():
                    IraEstados=self.automataAFN.irA(s,caracter)
                    if self.is_empty(IraEstados):
                        for Estados in IraEstados:
                            if self.equal(Ss,Estados)==0:
                                Saux.add(EstadosConjuntoAux.setConjuntos(Estados)) #Como haces un new Conjuntos() como en Java ? Si no se puede tendre que crear una lista de Objetos Conjuntos posiblemente
                                # Sí, sí se puede, así tal cual :p
                                # Saux.add(Conjuntos())
                s.setbanderacheck(0)
                return self.transformarAFNtoAFD(Saux)
                     
    def is_empty(self,conjunto):
        return len(conjunto)!=0

    def getEstadosConjunto(self):
        return self.EstadosConjunto
    #Verificamos si existe un conjunto dentro de nuestro conjunto de estados principales
    def equal(self,SConjunto,IraConjunto):

        for S in SConjunto:
            if(S.getConjunto()==IraConjunto):
                return 1

        return 0
    
    #Retorna el Estado AFD principal esta es el primer metodo que debes de llamar y pasar como parametro a transformarAFNtoAFD
    def getSsuper(self):
        Ss=set()
        return Ss.add(self.EstadosConjunto)