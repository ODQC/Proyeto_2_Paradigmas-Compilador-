import sys
import AnalizadorLexico
import Parser
import Checker
import ImprimirArbol
import AST

Matriz = []

class Controlador():
    """ Clase Controladora recibe el archivo a abrir luego
          se verifica si se puede abrir o no
          En caso de que si sea valido se procede con el Scanner
    """

    
    def __init__(self, archivo):
        self.texto = archivo

    def verificar_Archivo(self):
         try:
             exprs = open(self.texto, "r")
             self.texto=exprs
             return 1       
         except OSError as err:
             print("OS error: {0}".format(err))
             return 0
            
    def get_Archivo(self):
        return self.texto


    
        
    
