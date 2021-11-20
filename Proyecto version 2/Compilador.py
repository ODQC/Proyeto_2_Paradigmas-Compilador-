import sys
import Scanner
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


#**********************************************************************

def compilar():

    f = "test.txt"
    controlador= Controlador(f)
    i= controlador.verificar_Archivo()
    if i ==1:
        sc=Scanner
     
        Tokens = sc.verificar_Scanner(controlador.get_Archivo())
        sc.getReportErrors()
        print (Tokens)
        if(sc.getReportErrors()==0):
            Tree = Parser.iniciar_Parser(Tokens)
            if (Parser.get_reportErrors() is True):
                
              
                print("\n\n*********************************************************\n----------> Inicio proceso ANALISIS SEMANTICO\n\n")
                visitor=Checker.Checker()
                Checker.Checker.check(Tree)
                

                print("\n\nImprimiendo arbol decorado...\n----------------------------------------------------------------\n")
                impresion = ImprimirArbol.ImprimirArbol(Tree)
                impresion.imprime_Arbol(Tree)

            else:
                print ("--------------------------------------------------")
        else:
            print("\n---------------------------------------------------\n Se obtuvieron errores en el analisis sintactico")


        
    
        
    
