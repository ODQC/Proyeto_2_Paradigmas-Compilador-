#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Implementacion del analisis semantico para
lenguaje minitriangulo basado en el libro de Watt '''

from AST import *
from IdentificationTable import *
from Type import *

idTable=IdentificationTable() # obtener objeto de la clase identificationTable
sectionBSS = "section .bss \n\n"
sectionDATA = "section .data \n\n msg db "" 0xA \n len equ  $ - msg \n guardar dd 00 \n"
sectionTEXT = "section .text \n\n global _start \n\n _start: \n\n"

class Checker():


    def __init__(self):
        '''
            se definen los tipos int y bool luego se
            ingresan a la tabla la cual es un diccionario los
            valores correspondientes donde 0 es booleano
            1 entero y -1 es error
        '''
        
        self.Int = Type(1) ## corresponde al int
        self.Bool = Type(0)## corresponde al booleano
        self.Error = Type(-1) ## corresponde al error
        self.Func =Type(2)
        

        idTable.enter("true",self.Bool) # se ingresan los valores llave, valor al diccionario
        idTable.enter("false",self.Bool)# se ingresan los valores llave, valor al diccionario
        idTable.enter("Integer",self.Int)# se ingresan los valores llave, valor al diccionario
        idTable.enter("Boolean",self.Bool)# se ingresan los valores llave, valor al diccionario
        idTable.enter("putint",self.Func)# se ingresan los valores llave, valor al diccionario
        
    
    def check(AST):
        ''' se implementa el visitor '''
        
        AST.visit(AST,None)

    def visitProgram(self,o):
        global sectionTEXT
        ''' recibe un programm y se encarga de visitar a la clase  command'''
        self.command.visit(self,o)
        '''Agrega los valores necesarioa en el section .text'''
        sectionTEXT+=" jmp salida"
        if ( "imprimir" in sectionTEXT):
            sectionTEXT+="\n\n imprimir:\n mov eax,4\n mov ebx,1 \n int 0x80 \n ret"
        sectionTEXT+= "\n\n salida:\n mov eax,1 \n int 0x80 \n"
        escribirArchivo()
        return None

    def visitLetCommand(self,o): ##
        '''
            En el letCommand es donde se encarga de
            abrir el scope en donde se aumenta un nivel al scope
            definido en identificationTable, tambien se realizan los
            respectivos visit de acuerdo a las reglas de produccion del
            lenguaje minitriangulo y finalmente se cierra el scope
            donde se disminuye un nivel al scope
        '''
        identificationTable=getIDTabla() #aumenta nivel
        identificationTable.openScope()
        self.declaration.visit(self, None)
        self.command.visit(self, None)
        identificationTable.closeScope()#disminuye nivel
        return None

    def visitSequentialDeclaration(self,o): #
        '''
        Metodo en el que se realizan los visit correspondientes
        de acuerdo al sequentialDeclaration , declaracion  1 y 2
        , para seguir recorriendo el arbol ast
        '''
        self.decl1.visit(self,None)
        self.decl2.visit(self,None)
        return None

    def visitConstDeclaration(self,o): #####
        '''
        Metodo en el que se realizan los visit correspondientes
        de acuerdo al ConstDeclaration  identificador y expression
        , para seguir recorriendo el arbol, tambien se
        verifica si la variable ya existe
        ejemplo:

                const n ~ 5;#
                const n ~ 4;# repeticion
                const b ~ 4
        Ademas se encarga de ir metiendo los datos necesarios en la seccion .data
        Por ejemplo se mete el identificador : si es const r ~ 20 lo mete como r : dd y el valor se lo asinga en el visit expression correspondiente
        '''
        global sectionDATA
        identifier=self.identificador.identificador
        sectionDATA = sectionDATA + identifier + ": dd "
        self.identificador.visit(self,None)
        etype = self.expression.visit(self,None)
        try:
            sectionDATA=sectionDATA+str(self.expression.value)
            sectionDATA=sectionDATA+"\n"
        except:
            pass
        
        if(getIDTabla().enter(identifier,self)==False):
            print("Error, la variable ya esta declarada")
  
        return None

    def visitVarDeclaration(self,o): ## 
        '''
        Metodo en el que se realizan los visit correspondientes
        de acuerdo al VarDeclaration  identificador y expression
        , para seguir recorriendo el arbol, tambien se
        verifica si la variable ya existe
        ejemplo:

                var n : a;#
                var n : c;# repeticion
                const b ~ 4
        Ademas se encarga de ir metiendo los datos necesarios en la seccion .data
        Por ejemplo se mete el identificador : si es var r : Integer lo mete como r : dd y el valor se lo asinga en el visit expression correspondiente
        '''
        global sectionDATA
        identifier = self.identificador.identificador
        sectionDATA = sectionDATA + identifier + ": dd "
        self.identificador.visit(self,None)
        self.type_denoter.visit(self,None)
        sectionDATA=sectionDATA+"\n"
        if(getIDTabla().enter(identifier,self)==False):
           print("Entro, la variable ya esta declarada")
       
        return None

    def visitIntegerExpression(self,o):   #Y
        '''
        El visitIntegerExpression se encarga de decorar el
        arbol cuando se trata de un entero
        
        '''
        self.type = getInt()    
        return self.type


    def visitTypeDenoter(self,o):
        '''
        Metodo en el que se realizan los visit correspondientes
        de acuerdo al TypeDenoter, en este caso el identificador para obtener
        el nombre o tipo de TypeDenoter, se encarga de asingar un 0 a la hora de
        realizar la generacion de codigo ( ejemplo var n : Integer seria n dd 0 )
        Hace las validaciones necesarias para verificar si el TypeDenoter es un bool o int
        de lo contrario imprime el error
        '''
        global sectionDATA
        vTypeDenoter = (self.identificador.visit(self,None))
        sectionDATA = sectionDATA + "0" 
        if(vTypeDenoter!=None):
           
            if (vTypeDenoter.equals(getBool())):
                self.identificador.type = getBool()
                self.type = getBool()
                return getBool()
            elif (vTypeDenoter.equals(getInt())):
                self.identificador.type = getInt()
                self.type = getInt()
                return getInt()

            elif(vTypeDenoter.equals(getError())):
                print("Error 1 contextual, typeDenoter no definido")
                return getError()
        else:
            print("Error 2 contextual, typeDenoter no definido")

    def visitIdentifier(self,o):
        '''
        Metodo en el que se obtiene el identificador que se esta analizando
        y se busca en la tabla de simbolos o diccionario con su correspondiente scope
        '''
        tipoId = self.identificador
        if(getIDTabla().verificarExistencia(tipoId)):
            try:
                return getIDTabla().tabla[self.identificador,getIDTabla().scope]
            except:
                pass
        elif(getIDTabla().verificarAmbienteEstandar(tipoId)):
            try:
                return getIDTabla().tabla[tipoId,0]
            except:
                pass
        else:
            return None

    def visitSequentialCommand(self,o):
        '''
        Metodo en el que se visita los dos commands correspondientes
        '''
        self.command1.visit(self, None);
        self.command2.visit(self, None);
        return None

    def visitAssignCommand(self,o): # ya esta
        '''
        Metodo en el que el tipo de la variable o identificador y se obtiene el tipo de la expression
        '''
        vType = self.variable.visit(self,None)
        eType = self.expression.visit(self,None)
        '''
        Si los tipos no corresponden, imprime error
        '''
        if(vType.type != -1 and eType.type != -1):
            if(not vType.equals(eType)):
                print("Error ,AssignCommand no es valido")
                    
        return None

    def visitBinaryExpression(self,o):
        '''
        Metodo en el que el tipo de la expression 1 y se obtiene el tipo de la expression 2, ademas de la declaracion
        '''
        lista = [">","<"]
        eType1 = self.expr1.visit(self,None) 
        eType2 = self.expr2.visit(self,None) 
        declaration = self.oper.visit(self,None) 
        '''
        Se verifica si las dos expressiones son bool o si las dos son int, de lo contrario imprime error
        '''
        if(igualarTipos(eType1,eType2)==True):
            self.type= getBool()
        elif(igualarTiposInt(eType1,eType2)==True):
            self.type = inLista(self,lista,declaration)
        else:
            print("Error en analisis semantico, operadores distintos.")
            self.type= getError()
        return self.type


    def visitVnameExpression(self,o):
        '''
        Metodo en el que se visita el nombre de la variable o vname
        '''
        nodo = self.variable.visit(self,None)
        '''
        Si es none es que no se encuentra definida, de lo contrario se obtiene el tipo si es const declaration o var declaration y al final se retorna el tipo
        '''
        if(nodo == None):
            self.type = getError()
            print("Error contextual, el Vname no se encuentra definido. ")

        elif( nodo.getName() == "ConstDeclaration"):
              self.type=nodoConstDeclaration(nodo,self)
                  
        elif( nodo.getName() == "VarDeclaration"):
            self.type=nodoVarDeclaration(self,nodo)

        else:
            self.type = nodo
            
        return self.type
    
###############################################
    
    def visitNombreIdentificador(self,o):
        '''
        Metodo en el que se obtiene el tipo del identificador
        '''
        tipo = self.type
        return tipo

    
    def visitCallCommand(self,o):
        '''
        Metodo en el que se visita el identificador del call command y su expression y se valida si ese call command es un print
        '''
        comparePrint(self.identificador.identificador,self.expression.identificador)
        ident = self.identificador.visit(self,None) 
        exp1 = self.expression.visit(self,None)
        return None

    
    def visitIfCommand(self,o):
        '''
        Metodo en el que se obtiene el tipo de la expression
        '''
        tipoExp = self.expression.visit(self,None)
        '''
        Si la exp no es bool, imprime error
        '''
        if(not tipoExp.equals(getBool())):
            print("Error contextual, la expresion del if no es booleana")
        '''
        Se visita los dos command que proceden del if (then command else command)
        '''   
        self.command1.visit(self,None)
        self.command2.visit(self,None)
        return None

    def visitForCommand(self,o):
        '''
        Metodo en el que se visita la primera expression del for y la segunda expression del for y se obtiene sus dos identificadores
        '''
        global sectionTEXT
        variable1= self.expr.variable.identificador
        variable2= self.expr2.variable.identificador
        '''
        Se hace la generacion de codigo para el for
        '''
        valorFor= "\n mov esi,["+variable1+"]\n\ninicio"+ str(0)+":\n add esi,1 \n cmp esi,["+variable2+"]"+ "\n jb inicio"+str(0)+"\n"
        sectionTEXT+= valorFor
        '''
        Se obtiene el tipo de ambas expressiones del for
        '''
        tipoExp = self.expr.visit(self,None)
        tipoExp2 = self.expr2.visit(self,None)
        '''
        Si amabas no son int, imprimer error ( for int in lim int ) (for 2 in lim 10)
        '''
        if(not tipoExp.equals(getInt()) or not tipoExp2.equals(getInt())):
            print("Error contextual, la expresion del for no es int")
        
        return None

    def visitWhileCommand(self,o):
        '''
        Metodo en el que se el tipo de la expression del while
        '''
        tipoExp = self.expression.visit(self,None)
        '''
        Si no es bool, imprime error
        '''
        if(not tipoExp.equals(getBool())):
            print("Error contextual, la expresion del While no es booleana")

        '''
        Se visita el command ( while bool do command)
        '''
        self.command.visit(self,None)
        return None
    

    def visitUnaryExpression(self,o):
        '''
        Metodo en el que se obtiene el tipo de la expression del UnaryExpression y se visita al operador y se obtiene
        '''
        tipoExpression = self.expression.visit(self,None)
        operador = self.operator.visit(self,None)
        return tipoExpression  


#####################################
    
def getIDTabla():
    '''Funcion en la cual se retorna
    la tabla de simbolos utilizada'''
    return idTable

def getInt():
    '''se retorna el objeto de  tipo entero
    '''
    return Type(1)

def getBool():
    '''se retorna el tipo de bool'''
    return Type(0)

def getError():
    '''se retorna el tipo error'''
    return Type(-1)

def getFunc():
    '''se retorna el tipo de  func'''    
    return Type(2)

def setTabla(tabla):
    '''
    Se setea la tabla
    '''
    idTable=tabla

def imprimirTabla():
    '''
    Metodo para imprimir la tabla de simbolos o diccionario
    '''
    print(idTable.tabla)


###############################################
def nodoConstDeclaration(nodo,self):
    '''
    Metodo en el que se obtiene el tipo del identificador del const declaration
    '''
    Type=None
    try:
        Type = nodo.expression.variable.identificador
                  
    except:
        pass
    '''
    Si el tipo es false o true , se devuele Boolean, de lo contrario se devuelve el tipo correspondiete (int)
    '''           
    if(Type=="false" or Type=="true"):
        self.type= getBool()
    else:
        self.type = nodo.expression.type
                  
    self.typeInstance = False
    return self.type
    
#########################################
def nodoVarDeclaration(self,nodo):
    '''
    Metodo en el que se obtiene el tipo del identificador y valida si es integer o boolean y retorna el tipo
    '''
    self.type = nodo.type_denoter.identificador.type
    if(self.type=="Integer"):
        self.type = getInt()
    elif(self.type=="Boolean"):
        self.type = getBool()
    
                
    self.typeInstance = True
    return self.type
#########################################

def igualarTipos(eType1,eType2):
    '''
    Metodo en el que se valida si ambas expressiones son boolean
    '''
    if (eType1.equals(getBool()) and eType2.equals(getBool())):
        return True
    else:
        return False
    
#########################################

def igualarTiposInt(eType1,eType2):
    '''
    Metodo en el que se valida si ambas expressiones son Integer
    '''
    if (eType1.equals(getInt()) and eType2.equals(getInt())):
        return True
    else:
        return False

##########################################
def inLista(self, lista, declaration):
    '''
    Metodo en el que se valida si la delcaracion esta en la lista que se le manda y retorna su tipo
    '''
    if(declaration in lista):
        self.type=getBool()
        return self.type
    else:
        self.type= getInt()
        return self.type

def escribirArchivo():
    '''
    Metodo en el que se escribe en un archivo.asm el codigo generado, agregando cada una de las secciones que se fueron armando durante el recorrido
    '''
    global sectionBSS
    global sectionDATA
    global sectionTEXT
    file = open("generado.asm","w")
    file.write(sectionDATA)
    file.write(sectionBSS)
    file.write(sectionTEXT)
    file.close() 
        
def comparePrint(variable,identificador):
    '''
    Metodo en el que se valida si se esta recorriendo un print y genera el codigo respectivo para el print
    '''
    global sectionTEXT
    if(variable == "print"):
        sectionTEXT+=" mov esi,["+identificador+"]"+"\n add esi,'0' \n mov[guardar],esi \n mov ecx,guardar \n mov edx,4\n call imprimir\n"
        #print(sectionTEXT)    
