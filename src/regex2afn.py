from convertidorPostfijo import *

class regex2afn(object):
    """Clase que se encarga de convertir expresiones regulares a AFNs a través de un analizador léxico

        Args:
            anlex (AnalizadorLexico): El analizador léxico que contiene el AFD a utilizar para la evaluación de las cadenas sigma
    """
    def __init__(self, anlex: AnalizadorLexico):
        self._anlex = anlex
        self._afn = None
    
    ''' Atributos
    '''
    @property
    def anlex(self):
        """El analizador léxico que contendrá la tabla AFD

        Returns:
            AnalizadorLexico: El objeto asociado a este atributo
        """
        return self._anlex
    @anlex.setter
    def anlex(self, value):
        self._anlex = value
    @property
    def afn(self):
        return self._afn
    @afn.setter
    def afn(self, value):
        self._afn = value

    ''' Métodos
    '''
    def convertirRegex(self):
        pass