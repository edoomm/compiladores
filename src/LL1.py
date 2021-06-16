from gramaticas import *

class LL1(object):

    def __init__(self, gramatica=None):
        self.Vn             = set()
        self.Vt             = set()
        self.listaReglas    = [] if gramatica == None else gramatica._ListaReglas
        self.tokens         = {}
        self.tabla          = []
        self.cabcol         = []
        self.cabfil         = []

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
                if not dato in self.Vn and dato != "EPSILON":
                    self.Vt.add(dato)

    def first(self,lista :list,simbolos :set):
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
                            self.first(f,simbolos)
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
                            self.first(listAux,conjunto)
                            listAux=[]
        else:
            for fila in self.listaReglas:
                for i in range(len(fila)):
                    if i!=0:
                        
                        if lista[0]==fila[i] and i<len(fila)-1 and fila[0]!=lista[0]:
                            
                            listAux.append(fila[i+1])
                            
                            self.first(listAux,conjunto)
                            listAux=[]
                            listAux.append(fila[0])
                            
                            self.follow(listAux,conjunto)
                            listAux=[]
                        elif lista[0]==fila[i] and i==len(fila)-1 and fila[0]!=lista[0]:
                            
                            self.follow(fila,conjunto)
        if "EPSILON" in conjunto:
            conjunto.remove("EPSILON")
        
        return conjunto
 
    def asignarTokens(self, esexpnum = False):
        """Asigna los tokens de la gramática de gramáticas con la gramática de entrada

        Args:
            esexpnum (bool, optional): Sirve para asignar automaticamente los tokens de enum.txt. Defaults to False.
        """
        if esexpnum == False:
            for terminal in self.Vt:
                self.tokens[terminal] = input("Ingrese el token para '" + terminal + "': ")
        else:
            self.tokens = {'ENTRE': '40', 'MENOS': '20', 'MAS': '10', 'P_D': '60', 'NUM': '70', 'P_I': '50', 'POR': '30'}

    def construirTabla(self):
        """Construye la tabla de análisis sintáctico LL(1)
        """
        self.cabcol = list(self.tokens.values())
        self.cabcol.append("$")

        self.cabfil = list(self.Vn) + self.cabcol

        colaux = [''] + self.cabcol
        self.tabla.append(colaux)
        flg = 0
        for fila in self.cabfil:
            f = [fila] + [-1 for i in range(0, len(self.cabcol))]
            if fila == self.cabcol[flg] and fila != "$":
                f[flg + 1] = "pop"
                flg += 1
            elif fila == "$":
                f[flg + 1] = "acep"
                flg += 1
            self.tabla.append(f)

        self.analizarReglas()

    def analizarReglas(self):
        """Analiza las reglas una por una para construir la tabla de análisis sintáctico LL1
        """
        num = 1
        for regla in self.listaReglas:
            lst = regla[1: len(regla)]
            cols = self.first(lst, set())
            if len(cols) == 0: # Significa que fue EPSILON el first
                cols = self.follow([regla[0]], set())
            for col in cols:
                fila = self.cabfil.index(regla[0]) + 1
                if col != "$":
                    columna = self.cabcol.index(self.tokens[col]) + 1
                else:
                    columna = len(self.cabcol)
                
                # Se remplaza por tokens numéricos
                i = 0
                while i < len(lst):
                    if lst[i] in self.tokens.keys():
                        lst[i] = self.tokens[lst[i]]

                    i+=1
                self.tabla[fila][columna] = [lst, num]
            num += 1
      
    def imprimirTabla(self):
        """Imprime la tabla de análisis sintáctico LL(1)
        """
        print(end='\t')
        for cabecera in list(self.tokens.keys()):
            print(cabecera, end='\t')
        print("")
        for fila in self.tabla:
            for celda in fila:
                print(celda, end='\t')
            print("")

#################################################################################################
#   TEST SECTION                                                                                #
#################################################################################################

# analizador = AnalizadorLexico("grams")
# op = 12
# cadena = "E->T E';E'->MAS T E'|MENOS T E'|EPSILON;T->F T';T'->POR F T';T'->ENTRE F T'|EPSILON;F->P_I E P_D|NUM;"
# analizador.CadenaSigma = input("\nCadena a analizar: ") if op == 1 else cadena
# if op != 1:
#     print("\nCadena a analizar:", cadena, "\n")

# gx2 = GramaticasDeGramaticas(analizador)
# if gx2.inieval():
#     anll1 = LL1(gx2)
#     anll1.llenarVnAndVt()

#     anll1.asignarTokens(esexpnum=True)
#     anll1.construirTabla()

#     anll1.imprimirTabla()
# else:
#     print("INCORRECTO")