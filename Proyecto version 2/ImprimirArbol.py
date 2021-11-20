from AST import *
import Type
'''
Clase que se encarga de hacer la impresion del arbol sintactico abstracto
'''
class ImprimirArbol():
   
    '''
    Constructor de la clase ImprimirArbol con su unico atributo arbol
    '''
    def __init__(self,arbol):
        
        self.tree=arbol

    '''
    Funcion que se encarga de imprimir el arbol, recorre los hijos del arbol
    y va imprimiendo cada uno de ellos , con sus respectivos tipos
    '''
    
    def imprime_Arbol(self,arbol,identificador=0):
    
        if(isinstance(arbol, Expression) and arbol.type  != None or isinstance(arbol, TypeDenoter) and arbol.type != None ):
            variable="Func"
            tipo=self.imprimirTipo(variable,arbol)                
            mensaje1= identificador*"- "+str(type(arbol).__name__)+"  :  "+str(tipo)
            print (mensaje1)
            with open('mensaje2.txt', 'a') as f:
                f.write(mensaje1)
                f.write('\n')
  
        else:
            mensaje2=identificador*"- "+str(type(arbol).__name__)
            print(mensaje2)
            with open('mensaje2.txt', 'a') as f:
                f.write(mensaje2)
                f.write('\n')
            #arbolMensaje.append(mensaje2)

            
        '''
        Recorrido de los hijos del arbol
        '''
        for x in arbol.get_Hijos():
            if (isinstance(x,Nodo)):
       
                self.imprime_Arbol(x,identificador+1)
            else:
                identificador+=1
                
                mensaje3=identificador*"- "+str(x)
                print(mensaje3)
                with open('mensaje2.txt', 'a') as f:
                    f.write(mensaje3)
                    f.write('\n')
    
    



    '''
    Funcion que se encarga de decorar el arbol con su respectivo tipo
    '''
    def imprimirTipo(self,variable,arbol):
        if(str(arbol.type.type)=='1'):
            variable="Integer"
        elif(str(arbol.type.type)=='0'):
            variable="Boolean"
        elif(str(arbol.type.type)=='-1'):
            variable="Error"
        return variable
        
        
