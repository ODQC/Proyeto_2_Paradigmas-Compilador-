from Checker import *
from IdEntry import *

####################################################################
class Nodo(object):

    def __init__(self):
        pass
####################################################################

class Program(Nodo):

    '''
    Constructor de la clase program con sus atributos command y type
    '''
    def __init__(self, command):
        self.command = command
        self.type=None

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.command]

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitProgram(self,o)

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__

######################################################################
    

class Command(Nodo):
   pass

######################################################################

class Identificador(Nodo):
   '''
   Constructor de la clase Identificador con sus atributos variable, type e identificador 
   '''  
   def __init__(self, identificador):
       self.identificador = identificador
       self.variable=None
       self.type=None

   '''
   Funcion visit para visitar un nodo y saber que tiene dentro de el
   '''
   def visit(self,AST,o):
        return Checker.visitIdentifier(self,o)

   '''
   Funcion que retorna los hijos de la clase
   '''
   def  get_Hijos(self):
       return [self.identificador]
   '''
   Funcion que obtiene el nombre de la clase y la retorna
   '''
   def getName(self):
        return self.__class__.__name__
#########################################################################

class AssignCommand(Command):
    '''
    Constructor de la clase AssignCommand con sus atributos type, expression, variable 
    '''
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitAssignCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.variable,self.expression]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__

##########################################################################
    
class CallCommand(Command):
    '''
    Constructor de la clase CallCommand con sus atributos identificador, expression, type 
    '''
    def __init__(self, identificador, expression):
        self.identificador = identificador
        self.expression = expression
        self.type =None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitCallCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.identificador,self.expression]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class SequentialCommand(Command):
    '''
    Constructor de la clase SequentialCommand con sus atributos command1, command2 y type
    '''
    def __init__(self, command1, command2):
        self.command1 = command1
        self.command2 = command2
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitSequentialCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.command1,self.command2]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class IfCommand(Command):
    '''
    Constructor de la clase IdCommand con sus atributos command1, command2 y type
    '''
    def __init__(self, expression, command1, command2):
        self.expression = expression
        self.command1 = command1
        self.command2 = command2
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitIfCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.expression,self.command1,self.command2]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class WhileCommand(Command):
    '''
    Constructor de la clase WhileCommand con sus atributos command, expression y type
    '''
    def __init__(self, expression, command):
        self.expression = expression
        self.command = command
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitWhileCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.expression,self.command]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class ForCommand(Command):
    '''
    Constructor de la clase ForCommand con sus atributos expression, expression2 y type
    '''
    def __init__(self, expression, expression2):
        self.expr = expression
        self.expr2 = expression2
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitForCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.expr,self.expr2]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__

############################################################################
    
class LetCommand(Command):
    '''
    Constructor de la clase LetCommand con sus atributos command, declaration y type
    '''
    def __init__(self, declaration, command):
        self.declaration = declaration
        self.command = command
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitLetCommand(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.declaration, self.command]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
'''
class BnameOperatorDeclaration(self):
    Constructor de la clase BnameOperator con sus int1 int2 y int3
    def __init__(self,entero1,entero2,entero3):
                
            self.int1=entero1
            self.int2=entero2
            self.int3=entero3
    '''        

############################################################################

class Expression(Nodo):
    '''
    Constructor de la clase Expression con sus atributos type
    '''
    def __init__(self):
        self.type=None
    
############################################################################

class IntegerExpression(Expression):
    '''
    Constructor de la clase IntegerExpression con sus atributos value y type
    '''
    def __init__(self, value):
        self.value = value
        self.type=None
    
    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitIntegerExpression(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.value]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class VnameExpression(Expression):
    '''
    Constructor de la clase VnameExpression con sus atributos variable, typeInstance y type
    '''
    def __init__(self, variable):
        self.variable = variable
        self.type=None
        self.typeInstance=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitVnameExpression(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.variable]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class UnaryExpression(Expression):
    '''
    Constructor de la clase UnaryExpression con sus atributos operator, expression y type
    '''
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitUnaryExpression(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.operator,self.expression]

    def setUnaryExpression(tipo):
        self.type=tipo

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class BinaryExpression(Expression):
    '''
    Constructor de la clase BinaryExpression con sus atributos expr1, expr2, oper y type
    '''
    def __init__(self, expr1, oper, expr2):
        self.expr1 = expr1
        self.oper  = oper
        self.expr2 = expr2
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitBinaryExpression(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.expr1,self.oper,self.expr2]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class Vname(Nodo): 
    '''
    Constructor de la clase Vname con sus atributos identificador y type
    '''
    def __init__(self, identifier):
        self.identificador = identificador
        self.type=None

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.identificador]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__

############################################################################
    
class Declaration(Nodo):
    
    pass
############################################################################

class ConstDeclaration(Declaration):
    '''
    Constructor de la clase ConstDeclaration con sus atributos identificador, expression y type
    '''
    def __init__(self, identificador, expression):
        self.identificador = identificador
        self.expression = expression
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitConstDeclaration(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.identificador,self.expression]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class VarDeclaration(Declaration):
    '''
    Constructor de la clase VarDeclaration con sus atributos identificador, typeDenoter y type
    '''
    def __init__(self, identificador, type_denoter):
        self.identificador = identificador
        self.type_denoter = type_denoter
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitVarDeclaration(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.identificador,self.type_denoter]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class SequentialDeclaration(Declaration):
    '''
    Constructor de la clase SequentialDeclaration con sus atributos decl1, decl2 y type
    '''
    def __init__(self, decl1, decl2):
        self.decl1 = decl1
        self.decl2 = decl2
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitSequentialDeclaration(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.decl1,self.decl2]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
    
class TypeDenoter(Nodo):
    '''
    Constructor de la clase TypeDenoter con sus atributos identificador y type
    '''
    def __init__(self, identificador):
        self.identificador = identificador
        self.type=None

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitTypeDenoter(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.identificador]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################

class Operador(Nodo):## operador 
    '''
    Constructor de la clase Operador con sus atributos type
    '''
    def __init__(self, tipo):
        self.type = tipo

    '''
    Funcion visit para visitar un nodo y saber que tiene dentro de el
    '''
    def visit(self,AST,o):
        return Checker.visitNombreIdentificador(self,o)

    '''
    Funcion que retorna los hijos de la clase
    '''
    def  get_Hijos(self):
        return [self.type]

    '''
    Funcion que obtiene el nombre de la clase y la retorna
    '''
    def getName(self):
        return self.__class__.__name__
############################################################################
