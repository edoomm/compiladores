
from gramaticas import *

class LL1(object):

    def __ini__(self):
        self.Vn=set()
        self.Vt=set()
        self.listaReglas=None

    def llenarVnAndVt(self,gramatica):
       self.listaReglas=gramatica.ListaReglas()
       i=0
       for fila in self.listaReglas:
           for dato in fila:
               if i==0:
                   self.Vn.add(dato)
                   i+=1
           i=0    
       for fila in self.listaReglas:
           for dato in fila:       
               for d in self.Vn:
                    if d != dato:
                        self.Vt.add(dato)
            

                


