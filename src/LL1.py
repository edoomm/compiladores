from gramaticas import *

class LL1(object):

    def __init__(self, gramatica=None):
        self.Vn             = set()
        self.Vt             = set()
        self.listaReglas    = [] if gramatica == None else gramatica._ListaReglas

    ''' Métodos
    '''
    def llenarVnAndVt(self):
        i=0
        for fila in self.listaReglas:
            for dato in fila:
                if i==0:
                    self.Vn.add(dato)
                    i+=1
            i=0
        for fila in self.listaReglas:
            for dato in fila:
                if not dato in self.Vn:
                    self.Vt.add(dato)

    def first(self, lista: list) -> set:
        """Se encuentra el primer terminal de una lista que describe una regla

        Args:
            lista (list): Lista que puede contener terminales y no terminales

        Returns:
            set: El conjunto de tokens que se calcularon del first
        """
        conjunto = set()
        if lista == None or len(lista) == 0:
            return None
        if lista[0] in self.Vt:
            conjunto.add(lista[0])
        else:
            for elem in self.listaReglas:
                if elem[0] == lista[0]:
                    conjunto += self.first(elem[1:len(elem)])
                    # Acá pienso que se debe descartar toda derivación que sea A -> A, porque si no, se hace recursivo el pedo xd
        return conjunto
    
    def first2(self,lista :list,simbolos :set):
        bandera=1   
        lexema=""
        if lista[0] in self.Vt:
           simbolos.add(lista[0])     
           return simbolos
        else: 
         for fila in self.listaReglas:
            if fila[0]!=lista[0]:
                bandera=0
                            
            if bandera==1:
               
               lexema=fila[1]
               
               if lexema in self.Vt:

                    simbolos.add(lexema)     
                    
               else:
                    for f in self.listaReglas:
                        if f[0]==lexema:
                            self.first2(f,simbolos)
                        #return simbolos  
            bandera=1
        return simbolos    
    
    def follow(self,lista: list,conjunto: set):
        listAux=[]
        if lista[0]==self.listaReglas[0][0]: #Checamos que sea el primer simbolo de la lista
            conjunto.add("$") #agregamos pesos a la lista REGLA1
            for fila in self.listaReglas: #Se buscara el first del lado derecho del primer simbolo
                for i in range(len(fila)):
                    if i!=0:
                        if lista[0]==fila[i] and i<len(fila)-1:
                            listAux.append(fila[i+1])
                            self.first2(listAux,conjunto)
                            listAux=[]
        else:
            for fila in self.listaReglas:
                for i in range(len(fila)):
                    if i!=0:
                        
                        if lista[0]==fila[i] and i<len(fila)-1 and fila[0]!=lista[0]:
                            
                            listAux.append(fila[i+1])
                            
                            self.first2(listAux,conjunto)
                            listAux=[]
                            listAux.append(fila[0])
                            
                            self.follow(listAux,conjunto)
                            listAux=[]
                        elif lista[0]==fila[i] and i==len(fila)-1 and fila[0]!=lista[0]:
                            
                            self.follow(fila,conjunto)
        if "EPSILON" in conjunto:
            conjunto.remove("EPSILON")
        
        return conjunto

    """
    
    
    
    def first2(self,lista :list,simbolos :set):
        bandera=1   
        lexema=""
        for fila in self.listaReglas:
            for i in range(len(fila)):
                if len(fila) == len(lista):
                    if fila[i] != lista[i]:
                        bandera=0
                else:
                    bandera=0    
            if bandera==1:
               
               lexema=fila[1]
               print(lexema)
               if lexema in self.Vt:
                    simbolos.add(lexema)     
                    return simbolos
               else:
                    for f in self.listaReglas:
                        if f[0]==lexema:
                            self.first2(f,simbolos)
                            
                    return simbolos 
            bandera=1
    """

                        

    """
    def follow(self, terminal: str) -> set:
        Calcula el follow de un símbolo terminal

        Args:
            terminal (str): El símbolo terminal

        Returns:
            set: Regresa el conjunto de tokens que se obtuvieron
        
        pass
    """    

#################################################################################################
#   TEST SECTION                                                                                #
#################################################################################################

analizador = AnalizadorLexico("grams")
op = 12
#cadena = "E->E MAS T|E MENOS T|T;T->T POR F|T ENTRE F|F;F->P_I E P_D|NUM;"
cadena = "E->T Ep;Ep->MAS T Ep|MENOS T Ep|EPSILON;T->F Tp;Tp->POR F Tp;Tp->ENTRE F Tp|EPSILON;F->P_I E P_D|NUM;"
analizador.CadenaSigma = input("\nCadena a analizar: ") if op == 1 else cadena
if op != 1:
    print("\nCadena a analizar:", cadena, "\n")

gx2 = GramaticasDeGramaticas(analizador)
if gx2.inieval():
    #gx2.imprimirListaReglas()
    
    anll1 = LL1(gx2)
    anll1.llenarVnAndVt()
    print("No terminales:", anll1.Vn, "\nTerminales:", anll1.Vt)
    #lista = anll1.listaReglas[0][3:len(anll1.listaReglas)]
    lista=["T"]
    print("Lista:", lista)
    con=set()
    anll1.follow(lista,con)
    
    print("Follow de lista:", con)
else:
    print("INCORRECTO")