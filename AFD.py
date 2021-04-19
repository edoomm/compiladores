from AFN import *
from io import open

class AFD(object):
    """Clase para representar un Automata Finito Determinista

    Args:
        afn (AFN, optional): Un AFN que puede ser pasado para convertirlo automáticamente a AFN. Defaults to None.
    """
    def __init__(self, afn=None):
        self._tabla = []
        self._afn = afn
        if self._afn != None:
            self.constructor1(afn)

    def __str__(self):
        tablastr = "AFD:\n"
        for fila in self.tabla:
            for col in fila:
                tablastr += str(col) + "\t"
            tablastr += "\n"
        return tablastr
    
    ''' Atributos
    '''
    @property
    def afn(self):
        return self._afn
    @afn.setter
    def afn(self, value):
        self._afn = value
    @property
    def tabla(self):
        return self._tabla
    @tabla.setter
    def tabla(self, value):
        self._tabla = value

    ''' Constructores
    '''
    def constructor1(self, afn):
        self.inicializarTabla()
        self.convertirAFN(afn)

    ''' Métodos
    '''
    def inicializarTabla(self):
        """Inicializa la tabla con la fila de los símbolos del alfabeto
        """
        header = self.afn.getAlfabeto().copy()
        header.insert(0, '')
        header.append("Edo Acept")

        self.tabla.append(header)

    def convertirAFN(self, afn):
        """Convierte un AFN a un AFD implementando la representación de la forma tabulada del AFD

        Args:
            afn (AFN): El AFN a convertir
        """
        sI = [] # Representará las S_{i}. s0, s1, s2, ...
        fila = [] # Lista auxiliar que representerá las filas de nuestra tabla
        # Se empieza con el estado inicial
        sI.append(afn.cerraduraEpsilon(afn.EdoIni)) # s0
        fila.append(len(sI)-1) # ID del estado
        # Después se itera sobre ese primer estado con todos los símbolos del estado
        for c in afn.getAlfabeto():
            saux = afn.irA(sI[0], c)
            if saux not in sI and len(saux) != 0: #verificas que el conjunto no esta en sI y que no este vacio
                sI.append(saux)
                fila.append(len(sI)-1)
            elif saux in sI:
                fila.append(sI.index(saux))
            else:
                fila.append(-1)
        fila.append(self.existeEdoAcept(sI[0])) # Edo Acept
        self.tabla.append(fila.copy())
        # Y ahora se itera sobre los sI que salieron de la primer iteración
        i = 1 # El índice irá de s1, s2, ..., sn
        l = len(sI) # La longitud que podrá ir cambiando si se agrega un nuevo estado
        while i != l:
            fila=[]
            fila.append(i)
            # Se itera sobre el alfabeto
            for c in afn.getAlfabeto():
                saux = afn.irA(sI[i], c)
                if saux not in sI and len(saux) != 0:
                    sI.append(saux)
                    fila.append(len(sI)-1)
                elif saux in sI:
                    fila.append(sI.index(saux))
                else:
                    fila.append(-1)
            fila.append(self.existeEdoAcept(sI[i]))
            self.tabla.append(fila.copy())
            # Se actualiza longitud e indice
            l = len(sI)
            i += 1

    def existeEdoAcept(self, cjto):
        """Determina si en un conjunto de estados existe un estado de aceptación

        Args:
            cjto (set): El conjunto de estados

        Returns:
            int: 1 en caso de ser estado de aceptación y no tener un token, si se tiene un token regresa el token, si no hay estados de aceptación, se regresa -1
        """
        for e in cjto:
            if e.aceptacion and e.token == -1:
                return 1
            elif e.aceptacion and e.token != -1:
                return e.token
        return -1

    def exportarAFD(self,nombre):
        filas=""
        archivoTexto=open(nombre+".txt","w")
        for fila in self.tabla:
            for col in fila:
                filas += str(col) + "\t"
            filas += "\n"
            archivoTexto.write(filas)
            filas=""
        archivoTexto.close()  

    
    #Algorigmo para importacion de AFD
    def importarAFD(self,nombre):
        archivoTexto=open(nombre+".txt","r") #abrimos el archivo txt y extraemos los datos por filas
        lineas=archivoTexto.readlines()
        archivoTexto.close()
        linea=[]        #Generamos una lista la cual contendra cada cadena que necesitemos
        linea.append("") 
        i=0     
        j=0
        numTxt="" #string para guardar numeros
        numeros="0123456789" #String que se ocupa para buscar numeros
        for l in lineas:       #Se itera sobra cada una de las lineas que nos arrojo el txt
            while i < len(l):   
                """
                    En esta parte del codigo se buscar limpiar la linea para solo insertar en la tabla
                    los caracteres que necesitamos, por lo cual tiene que pasar por todas estas validaciones
                """
                if str(l[i]) != '\t' and str(l[i]) != " " and str(l[i])!= "\n":
                    if l[i] == "-" and l[i+1]!="\t":
                        j=i
                        while l[j]!="\t":
                            numTxt+=l[j]
                            j+=1
                        i=j-1
                        linea.append(numTxt)
                        j=0
                        numTxt=""
                    elif numeros.find(l[i]) != -1 and l[i-1]!="-": 
                        j=i
                        while str(l[j])!="\t":
                            numTxt+=str(l[j])+""
                            j+=1 
                        i=j-1
                        linea.append(numTxt)
                        j=0
                        numTxt=""
                    elif l[i] == "E" and l[i+1]=="d":
                        linea.append("Edo Acept")
                        i=len(l)
                    else:
                       linea.append(l[i])
                i+=1
            """
                Finalmente en esta seccion es donde se ingresa un Salto de linea y se inserta en la tabla cada linea ya valida
            """
            
            self._tabla.append(linea)
            linea=[]
            i=0

# # PRUEBAS PARA CONVERSIÓN DE AFN ESPECIAL A AFD
# # Creación de AFNs básicos
a = AFN()
a.crearAFNBasico('+')
b = AFN()
b.crearAFNBasico('-')
c = AFN()
c.crearAFNBasico('*')
d = AFN()
d.crearAFNBasico('/')
e = AFN()
e.crearAFNBasico('(')
f = AFN()
f.crearAFNBasico(')')
# Creación de D.D = [0-9]+ o (. o [0-9]+)?
g = AFN()
g.crearAFNBasico('0', '9')
g.cerradurap()
h = AFN()
h.crearAFNBasico('.')
i = AFN(1)
i.crearAFNBasico('0', '9')
i.cerradurap()
h.concatenar(i)
h.opcional()
g.concatenar(h)

analizador = AnalizadorLexico()
analizador.union([a,b,c,d,e,f,g])
# analizador.afn.imprimir()

afd = AFD(afn=analizador.afn)
print("Digita el nombre del AFD: ")      
afd.exportarAFD(input())

afdDos=AFD()
print("Digita el nombre del AFD: ")  
afdDos.importarAFD(input())
#print(afdDos)


l=analizador.AnanalizarCadena("123.45+20*30(12)",AFD.tabla)

for e in l:
    print(e)