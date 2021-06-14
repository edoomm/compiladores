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

    def follow(self, terminal: str) -> set:
        """Calcula el follow de un símbolo terminal

        Args:
            terminal (str): El símbolo terminal

        Returns:
            set: Regresa el conjunto de tokens que se obtuvieron
        """
        pass


#################################################################################################
#   TEST SECTION                                                                                #
#################################################################################################

analizador = AnalizadorLexico("grams")
op = 12
cadena = "E->E MAS T|E MENOS T|T;T->T POR F|T ENTRE F|F;F->P_I E P_D|NUM;"
analizador.CadenaSigma = input("\nCadena a analizar: ") if op == 1 else cadena
if op != 1:
    print("\nCadena a analizar:", cadena, "\n")

gx2 = GramaticasDeGramaticas(analizador)
if gx2.inieval():
    gx2.imprimirListaReglas()
    
    anll1 = LL1(gx2)
    anll1.llenarVnAndVt()
    print("No terminales:", anll1.Vn, "\nTerminales:", anll1.Vt)
    lista = anll1.listaReglas[0][3:len(anll1.listaReglas)]
    print("Lista:", lista)
    # print("First de lista:", anll1.first(lista))
else:
    print("INCORRECTO")

simb = AFN()
simb.crearAFNBasico('a', 'z')
simb.unir(AFN(simbinf = "A", simbsup = "Z"))
# simb.concatenar(AFN(simbinf = 'a', simbsup = 'z').unir(AFN(simbinf='A', simbsup='Z')))
s2 = AFN(simbinf='a', simbsup='z')
s2.unir(AFN(simbinf='A', simbsup='Z')).unir(AFN(simbinf='0', simbsup='9')).unir(AFN(simbinf='_')).unir(AFN(simbinf="'"))
s2.cerradurak()
simb.concatenar(s2)
simb.unir(AFN(simbinf='♣'))

pc = AFN(simbinf=';')

flecha = AFN(simbinf='-')
flecha.concatenar(AFN(simbinf='>'))

orafn = AFN(simbinf="|") # No funciona con \|

esp = AFN(simbinf=' ')
esp.cerradurap()

# afd = AFD(simb)
# afd.exportarAFD("test")
# file = ""
# analizador = AnalizadorLexico("test" if file == "" else file)
analizador = AnalizadorLexico()
analizador.union([simb, pc, flecha, orafn, esp])
afd = AFD(analizador.afn)
afd.exportarAFD("test")