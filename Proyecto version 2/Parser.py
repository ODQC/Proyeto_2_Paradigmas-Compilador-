#Parser Mini Triangulo
#TEC - Costa Rica
#Compiladores e Interpretes
#Kevin Rodriguez - Josue Rodriguez - Alejandro Salas
from Scanner import *
from AST import *

#Lista con los simbolos terminales
lista = ["identificador", "int", "operador", "begin", "const", "do",
         "else", "end", "if", "in", "let", "then", "var", "while", "puntoycoma",
         "dospuntos", "dospuntosigual", "rabochancho", "parenIzquierdo", "parenDerecho", "eot","for","lim"]


#Lista con los operadores
operadores = ["+","-","*","/","<",">","=","\\"]

#Variables Globales
reportErrors=0
largo = 0
falta = False;
encontre = False;
exitoso = True;
ult = ""
primeraEntrada = False

#Arreglo Auxiliar
arregloID = ["let", "begin", "const", "do", "else", "end", "if",
             "in" ,"then", "var", "while", "Identificador", "Integer",
             " ", ";", ":=", ":", "~", "(", ")", "\000","for","lim"]

#Clase Token
#Esta clase se encargara de crear el token que se le manda para luego ser analizado
class Token:
    def __init__( self, tipoToken, sp) :
        self.token = tipoToken 
        self.sp2 = sp
        
#Clase Parser
#Esta clase sera la encargada de realizar el parseo del codigo
class Parser:

    #Constructor
    #Se encarga de llevar el arreglo de tokens enviado por el scanner
    #Se encarga de llevar la posicion actual del arreglo que se esta recorriendo
    #Se encarga de llevar el token actual que se va analizar
    def __init__(self, tokens):
        self.arreglo = tokens
        self.posicion = 0
        self.token_Actual = Token(21,"")

    ##################################################################################
    """ METODOS PARSE              METODOS PARSE                   METODOS PARSE """
    ##################################################################################

    #Funcion parse_Program
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Llama a la funcion single_Command para empezar el analisis
    def parse_Program(self):
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        PROGRAM = self.parse_Command()
        return Program(PROGRAM)


    #Funcion parse_Command
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Llama a la funcion single_Command para empezar el analisis
    #Verifica si lo que se esta analizando es un ; , lo que indica que se debe seguir analizando un single_command
    def parse_Command(self):
        try:
            self.arreglo[self.posicion].val
        except IndexError:
            self.arreglo[self.posicion-1].val
        SINGLE_COMMAND = self.parse_Single_Command()
        while (self.token_Actual.token == self.buscarLista("puntoycoma")):
            self.aceptarToken()
            SINGLE_COMMAND_AUX = self.parse_Single_Command()
            SINGLE_COMMAND = SequentialCommand(SINGLE_COMMAND,SINGLE_COMMAND_AUX)

        return SINGLE_COMMAND

    #Funcion parse_Single_Command
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Se encarga de ir verificando que tipo de single command es, retornando true si logro entrar a ese tipo de SC
    #Si retorna false, sigue buscando a cual tipo de SC pertenece
    #Si no entroe en ninguno, tira error de sintaxis , ya que deberia seguir un SC
    def parse_Single_Command(self):
        global primeraEntrada
        global encontre
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val

        if(self.token_Actual.token == self.buscarLista("identificador")):
            temp = self.parseSC1()
        elif(self.token_Actual.token == self.buscarLista("if")):
            temp = self.parseIf()
        elif(self.token_Actual.token == self.buscarLista("while")):
            temp = self.parseWhile()
        elif(self.token_Actual.token == self.buscarLista("for")):
            temp = self.parseFor()
        elif(self.token_Actual.token == self.buscarLista("let")):
            temp = self.parseLet()
        elif(self.token_Actual.token == self.buscarLista("begin")):
            temp = self.parseBegin()
        else:
            if(self.posicion == 0):
                exitoso = False;
                print("Linea : " + self.arreglo[self.posicion-1].pos)
                reportErrors+=1
                print ("Error de Sintáxis: El programa deberia empezar con un Single Command \n")

        return temp

    #Funcion parseSC1
    #Esta funcion se encarga de validar que se cumpla con la estructura Vname := Expression
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseSC1(self):
        global encontre
        global exitoso
        global arbol
        global reportErrors
        if(self.token_Actual.token == self.buscarLista("identificador")):
                ec2 = False;
            
                VALOR = self.arreglo[self.posicion].val
                
                IDENTIFICADOR = self.parse_Identificador()
                #print ("El arbol3 es : " + str(arbol))
                encontre = True
                if(self.token_Actual.token == self.buscarLista("dospuntosigual")):
                    ec2 = True;
                    self.aceptarToken()           
                    EXPRESSION = self.parse_Expression()
                    Vname= VnameExpression(IDENTIFICADOR)
                    
                    return AssignCommand(Vname, EXPRESSION)
                elif(self.token_Actual.token == self.buscarLista("parenIzquierdo")):
                    self.aceptarToken()
                    booleano = self.identificarPrint(VALOR)
                    EXPRESSION= self.parserExpressionIdentificador(booleano)
                   
            
                  #  EXPRESSION = self.parse_Expression()
                    if(self.token_Actual.token == self.buscarLista("parenDerecho")):
                        self.aceptarToken()
                        return CallCommand(IDENTIFICADOR, EXPRESSION)
                    else:
                        exitoso = False;
                        print("Linea : " + str(self.arreglo[self.posicion-1].pos))
                        reportErrors+=1
                        print ("Error de Sintáxis: Expresion le falta Paréntesis de cierre [ ) ] \n")
                else:
                    if(ec2 == False):
                        exitoso = False;
                        print("Linea : " + str(self.arreglo[self.posicion].pos))
                        reportErrors+=1
                        print("Error de Sintaxis: Assign Command le falta [ := ]" + "en lugar de: " + str(self.arreglo[self.posicion].val) + " \n")
                        return False;
                    else:
                        exitoso = False;
                        print("Linea : " + str( self.arreglo[self.posicion].pos))
                        reportErrors+=1
                        print ("Error de Sintáxis: Expresion le falta Paréntesis de inicio [ ( ] \n")
                        return False;
                return True
        return False

    def identificarPrint(self,valor):
    
        if(str(valor)== 'print'):
               return True
        return False

    def parserExpressionIdentificador(self,booleano):
        if(booleano == True):
  
            IDENTIFICADOR = self.parse_Identificador()
            return IDENTIFICADOR
        else:
            EXPRESSION = self.parse_Expression()
            return EXPRESSION
            

        
    
    #Funcion parseIf
    #Esta funcion se encarga de validar que se cumpla con la estructura if Expression then Single Command else Single Command 
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseIf(self):
        global encontre
        global exitoso
        global arbol
        global reportErrors
        if(self.token_Actual.token == self.buscarLista("if")):
                encontre = True
                self.aceptarToken()
                EXPRESSION = self.parse_Expression()
                if(self.token_Actual.token == self.buscarLista("then")):
                    self.aceptarToken()
                else:
                    exitoso = False;
                    print("Linea : " + str(self.arreglo[self.posicion].pos))
                    reportErrors+=1
                    print ("Error de Sintáxis : If le falta la palabra reservada [ then ] \n")
                COMMAND = self.parse_Single_Command()
                if(self.token_Actual.token == self.buscarLista("else")):
                    self.aceptarToken()
                else:
                    exitoso = False;
                    print("Linea : " + str(self.arreglo[self.posicion].pos))
                    reportErrors+=1
                    print ("Error de Sintáxis : If le falta la palabra reservada [ else ] \n")
                COMMAND_AUX = self.parse_Single_Command()
                return IfCommand(EXPRESSION, COMMAND, COMMAND_AUX)
        return False

    #Funcion parseWhile
    #Esta funcion se encarga de validar que se cumpla con la estructura while Expression do Single Command 
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseWhile(self):
        global encontre
        global arbol
        global exitoso
        global reportErrors
        if(self.token_Actual.token == self.buscarLista("while")):
                encontre = True
                self.aceptarToken()
                EXPRESSION = self.parse_Expression()
                if(self.token_Actual.token == self.buscarLista("do")):
                    self.aceptarToken()
                else:
                    exitoso = False;
                    b = int(self.arreglo[self.posicion].pos)-1
                    print("Linea : " + str(b))
                    reportErrors+=1
                    print ("Error de Sintáxis: While le falta la palabra reservada [ do ] \n")
                COMMAND = self.parse_Single_Command()
                return WhileCommand(EXPRESSION,COMMAND)
        return False



    #Funcion parseWhile
    #Esta funcion se encarga de validar que se cumpla con la estructura while Expression do Single Command 
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseFor(self):
        global encontre
        global arbol
        global exitoso
        global reportErrors
        if(self.token_Actual.token == self.buscarLista("for")):
                encontre = True
                self.aceptarToken()
                EXPRESSION = self.parse_Expression()
                if(self.token_Actual.token == self.buscarLista("in")):
                    self.aceptarToken()
                    if(self.token_Actual.token == self.buscarLista("lim")):
                        self.aceptarToken()
                     
                    else:
                        exitoso = False;
                        print("Linea : " + str(self.arreglo[self.posicion].pos))
                        reportErrors+=1
                        print ("Error de Sintáxis: For le falta la palabra reservada [lim] \n")
                else:
                    exitoso = False;
                    print("Linea : " + str(self.arreglo[self.posicion].pos))
                    reportErrors+=1
                    print ("Error de Sintáxis: For le falta la palabra reservada [ in ]  \n")
          
                EXPRESSION2 = self.parse_Expression()
                
                return ForCommand(EXPRESSION,EXPRESSION2)
        return False



    #Funcion parseLet
    #Esta funcion se encarga de validar que se cumpla con la estructura let Declaration in Single Command 
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseLet(self):
        global arbol
        global encontre
        global exitoso
        global reportErrors
        if (self.token_Actual.token == self.buscarLista("let")):
                encontre = True
                self.aceptarToken()
                DECLARATION  = self.parse_Declaration()
                if(self.token_Actual.token == self.buscarLista("in")):
                    self.aceptarToken()
                else:
                    exitoso = False;
                    b = int(self.arreglo[self.posicion].pos)-1
                    print("Linea : " + str(b))
                    reportErrors+=1
                    print ("Error de Sintáxis: let le falta la palabra reservada [ in ] \n")
                COMMAND = self.parse_Single_Command()
                return LetCommand(DECLARATION,COMMAND)
        return False


    def busqueda(self,s,lista,hijo):
        largo = len(s)
        if(hijo == 5):
            while(s != 0):
                if(s[largo - 1] == "]"):
                    texto = s[:largo-2] + "," + str(lista) + s[largo-2:]
                    break
                largo = largo - 1
        else:
            while(s != 0):
                if(s[largo - 1] == "'"):
                    texto = s[:largo+hijo] + "," + str(lista) + s[largo+hijo:]
                    break
                largo = largo - 1

        return texto
        
        

    #Funcion parseBegin
    #Esta funcion se encarga de validar que se cumpla con la estructura begin Command end 
    #Si cumple con la estructura continua, de lo contrario imprime el error correspondiente
    #Si no es este tipo de SC, retorna false
    def parseBegin(self):
        global encontre
        global exitoso
        global arbol
        global reportErrors
        if (self.token_Actual.token == self.buscarLista("begin")):
                self.aceptarToken()
                COMMAND  = self.parse_Command()
                if(self.token_Actual.token == self.buscarLista("end")):
                    self.aceptarToken()
                    return COMMAND
                else:
                    t = 0
                    ec = False;
                    for t in range(len(self.arreglo)):
                        if(self.arreglo[t].pos == "end"):
                            ec = True;
                            break;
                        else:
                            t = t + 1
                    if(ec == False):
                        b = self.arreglo[self.posicion-1].pos
                        b = int(b) + 1
                        exitoso = False;
                        print("Linea : " + str(b))
                        reportErrors+=1
                        print ("Error de Sintáxis: Begin deberia terminar con la palabra reservada [ end ] \n")
                return True
        return False


    #Funcion parse_Expression
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Llama a la parse_Primary_Expresion
    #Si lo que esta analizando es un operador, contina parseando con primary_Expression hasta que encuentre algo distinto
    def parse_Expression(self):
        global arbol
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        EXPRESSION = self.parse_Primary_Expression()
        while(self.token_Actual.token == self.buscarLista("operador")):
            OPERATOR = self.parse_Operator()
            EXPRESSION1 = self.parse_Primary_Expression()
            EXPRESSION = BinaryExpression(EXPRESSION,OPERATOR,EXPRESSION1)
        return EXPRESSION

    #Funcion parse_Primary_Expression
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Valida si el token es un Int, Identificador, Operador y lo parsea
    #Si es un (, valida que lo que este adentro sea una expresion valida y valida que al final cierre con )
    #De lo contrario imprime el error correspondiente
    def parse_Primary_Expression(self):
        global arbol
        global exitoso
        global arbol
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        if(self.token_Actual.token == self.buscarLista("int")):
            INTEGER = self.parse_Integer_Literal()
            return IntegerExpression(INTEGER)
        elif(self.token_Actual.token == self.buscarLista("identificador")):
            IDENTIFICADOR = self.parse_Identificador()
            return VnameExpression(IDENTIFICADOR)
        elif(self.token_Actual.token == self.buscarLista("operador")):
            OPERATOR = self.parse_Operator()
            EXPRESSION = self.parse_Primary_Expression()
            return UnaryExpression(OPERATOR, EXPRESSION)
        elif(self.token_Actual.token == self.buscarLista("parenIzquierdo")):
            self.aceptarToken()
            EXPRESSION = self.parse_Expression()
            if(self.token_Actual.token == self.buscarLista("parenDerecho")):
                self.aceptarToken()
                return Nodo.Expression()
            else:
                exitoso = False;
                self.token_Actual = self.scannear()
                print("Linea : " + str(self.arreglo[self.posicion-1].pos))
                reportErrors+=1
                print ("Error de Sintáxis: Expresion le falta Paréntesis de cierre [ ) ] \n")
        else:
            exitoso = False;
            self.token_Actual = self.scannear()
            b = self.arreglo[self.posicion-1].pos
            b = int(b) + 0
            print("Linea : " + str(b))
            reportErrors+=1
            print ("Error de Sintáxis: Expresion es invalida, no cumple con ser Identificador, Integer , Operador Expresion o ( EXpresion ) \n")

    #Funcion parse_Declaration
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Llama a la parse_Single_Declaration
    #Si lo que esta analizando es un ;, continua analizando hasta que encuentre algo distinto
    #Imprime el error de sintaxis correspondiente si no cumple
    def parse_Declaration(self):
        global exitoso
        global arbol
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        DECLARATION = self.parse_Single_Declaration()
        if(self.token_Actual.token != self.buscarLista("puntoycoma")):
            if(self.arreglo[self.posicion].val == "const" or self.arreglo[self.posicion].val == "var"):
                print("Linea : " + str(self.arreglo[self.posicion].pos))
                reportErrors+=1
                print ("Error de Sintáxis: Declaracion le falta [ ; ] \n")
                exitoso = False;
        tipo = self.buscarLista("puntoycoma")
        while (self.token_Actual.token == tipo):
            self.aceptarToken()
            DECLARATION_AUX = self.parse_Single_Declaration()
            DECLARATION = SequentialDeclaration(DECLARATION,DECLARATION_AUX)
            
        return DECLARATION
            
   

    #Funcion parse_Single_Declaration
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Valida que si es un const, que siga la estructura const Identificador ~ Expression
    #Valida que si es un var, que siga la estructura var Identificador : Type Denoter
    #Valida si hay un ; de mas
    #Imprime los errores de sintaxis correspondientes
    def parse_Single_Declaration(self):
        global exitoso
        global arbol
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        if(self.token_Actual.token == self.buscarLista("const")):
            self.aceptarToken()
            IDENTIFICADOR = self.parse_Identificador()
            self.aceptar(self.buscarLista("rabochancho"))
            EXPRESSION = self.parse_Expression()
            return ConstDeclaration(IDENTIFICADOR,EXPRESSION)
        elif(self.token_Actual.token == self.buscarLista("var")):
            self.aceptarToken()
            IDENTIFICADOR = self.parse_Identificador()
            self.aceptar(self.buscarLista("dospuntos"))
            TYPE_DENOTER = self.parse_Type_Denoter()
            return VarDeclaration(IDENTIFICADOR,TYPE_DENOTER)
        else:
       
            if(self.arreglo[self.posicion-1].val == ";"):
                 if(self.arreglo[self.posicion].val == "var" or self.arreglo[self.posicion].val == "const" or self.arreglo[self.posicion].val == "in" or self.arreglo[self.posicion].val == "begin" or self.arreglo[self.posicion].val == "if" or self.arreglo[self.posicion].val == "while" or self.arreglo[self.posicion].tipo == "Identificador" or self.arreglo[self.posicion].val == "for" ):
                     exitoso = False;
                     b = self.arreglo[self.posicion].pos
                     b = int(b) +- 1
                     print("Linea : " + str(b))
                     reportErrors+=1
                     print("Error de Sintaxis: Quitar el simbolo [;] \n")
                 else:
                     exitoso = False;
                     print("Linea : " + str(self.arreglo[self.posicion].pos))
                     reportErrors+=1
                     print ("Error de Sintáxis: Despues [ let ] deberia seguir un Single Declaration [ const ] o [ var ] \n")
                     self.aceptarToken()
                     self.parse_Identificador()
                     if(self.arreglo[self.posicion].val == "~"):
                          self.aceptar(self.buscarLista("rabochancho"))
                          self.parse_Expression()
                     else:
                          self.aceptar(self.buscarLista("dospuntos"))
                          self.parse_Type_Denoter()
            else:
                exitoso = False;
                print("Linea : " + str(self.arreglo[self.posicion].pos))
                reportErrors+=1
                print ("Error de Sintáxis: Despues [ let ] deberia seguir un Single Declaration [ const ] o [ var ] \n")
                self.aceptarToken()
                self.parse_Identificador()
                if(self.arreglo[self.posicion].val == "~"):
                     self.aceptar(self.buscarLista("rabochancho"))
                     self.parse_Expression()
                else:
                     self.aceptar(self.buscarLista("dospuntos"))
                     self.parse_Type_Denoter()
    #Funcion parse_Type_Denoter
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Llama a la funcion parse_Identificador
    def parse_Type_Denoter(self):       
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        IDENTIFICADOR = self.parse_Identificador()
        return TypeDenoter(IDENTIFICADOR)
        
    #Funcion parse_Identificador
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Valida que el token que se esta analizando es un identificador valido
    #De lo contrario imprime el error de sintaxis correspondiente
    def parse_Identificador(self):
        global exitoso
        global arbol
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        if (self.token_Actual.token == self.buscarLista("identificador")):
            N = self.arreglo[self.posicion].val
            
            self.token_Actual = self.scannear()
            NOMBRE = Identificador(N)
            return NOMBRE
        else:
            self.token_Actual = self.scannear()
            if(self.arreglo[self.posicion-4].val == "var"):
                exitoso = False;
                b = self.arreglo[self.posicion].pos
                b = int(b)
                print("Linea : " + str(b))
                reportErrors+=1
                print("Error de Sintaxis: [ var ] Tiene que terminar con un Type-denoter [ Identificador ] que sea valido \n")
            else:
                exitoso = False;
                print("Linea : " + str(self.arreglo[self.posicion].pos))
                reportErrors+=1
                print ("Error de Sintáxis: Identificador invalido \n")

    #Funcion Integer_Literal
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Valida que el token que se esta analizando es un int valido
    #De lo contrario imprime el error de sintaxis correspondiente
    def parse_Integer_Literal(self):
        global exitoso
        global arbol
        global reportErrors
            
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
        if (self.token_Actual.token == self.buscarLista("int")):
            NOMBRE = self.arreglo[self.posicion].val
            self.token_Actual = self.scannear()
            return NOMBRE
        else:
            self.token_Actual = self.scannear()
            exitoso = False;
            print("Linea : " + str(self.arreglo[self.posicion].pos))
            reportErrors+=1
            print ("Error de Sintáxis: No es un integer \n")

    #Funcion parse_Operador
    #Esta funcion se encarga de verificar primero que este entre los limites del arreglo
    #Valida que el token que se esta analizando es un operador valido
    #De lo contrario imprime el error de sintaxis correspondiente
    def parse_Operator(self):
        global exitoso
        global arbol
        global reportErrors
        try:
             self.arreglo[self.posicion].val
        except IndexError:
             self.arreglo[self.posicion-1].val
       
        if (self.token_Actual.token ==self.buscarLista("operador")):
            NOMBRE = self.arreglo[self.posicion].val
            self.token_Actual = self.scannear()
            return Operador(NOMBRE)
        else:
            exitoso = False;
            print("Linea : " + self.arreglo[self.posicion].pos)
            reportErrors+=1
            print ("Error de Sintáxis: No es un operador \n")



    ##################################################################################
    """ METODOS ACCEPT           METODOS ACCEPT                   METODOS ACCEPT """
    ##################################################################################
    
    #Funcion aceptarToken
    #Esta funcion se encarga de actualizar el token actual, escaneando el token en la posicion actual
    def aceptarToken(self):
        global reportErrors
        self.token_Actual = self.scannear()
        return
    
    #Funcion aceptar
    #Esta funcion recibe como parametro el token esperado, osea el token que deberia seguir
    #Analiza si el token actual es igual al que se le mando, y si lo es, lo pasa a escanear
    #Sino lo es, para a verificar que tipo era el esperado, para tirar el error correspondiente
    def aceptar(self,esperado):
        global exitoso
        global reportErrors
        if(self.token_Actual.token == esperado):
            self.token_Actual = self.scannear()
        else:
            if(esperado == self.buscarLista("rabochancho")):
                print("Linea : " + str(self.arreglo[self.posicion].pos))
                reportErrors+=1
                print("Error de Sintaxis: Esperaba el simbolo [ ~ ] antes de la expresion para [ const ] \n")
                exitoso = False
                self.token_Actual = self.scannear()
            elif((esperado ==  self.buscarLista("dospuntos"))):
                print("Linea : " + str(self.arreglo[self.posicion].pos))
                reportErrors+=1
                print ("Error de Sintaxis: Esperaba el simbolo [ : ] antes del identificador para [ var ] \n")
                exitoso = False;
                self.token_Actual = self.scannear()
            else:
                 print("ERROR")
                 reportErrors+=1
                 exitoso = False;
                 self.token_Actual = self.scannear()



    ##################################################################################
    """ METODOS SCAN              METODOS SCAN                   METODOS SCAN """
    ##################################################################################

    #Funcion scanAux
    #Esta funcion se encarga de identificar que tipo de token es, llamando a la funcion de identificar token
    #Crea el objeto token del tipo encontrado
    def scanAux(self):
        tipoToken = self.identificar_Token()
        return Token(tipoToken, "")

    #Funcion scannear
    #Esta funcion se encarga de aumentar la posicion del arreglo y verificar si ha llegado al fin del mismo
    #Tambien vuelve a identificar el tipo de token que es, llamando a la funcion de identificar token
    #Al final crea el objeto token del tipo encontrado
    def scannear(self):
        self.posicion += 1
        if (self.posicion == len(self.arreglo)):
            return Token(20,"")
        tipoToken = self.identificar_Token()
        return Token(tipoToken, "")


    ##################################################################################
    """ METODOS AUXILIARES      METODOS AUXILIARES           METODOS AUXILIARES """
    ##################################################################################
    
    #Funcion buscarLista
    #Esta funcion se encarga de buscar en la lista de palabras reservadas que tipo es
    #Devuelve un numero que sera el indice de donde esta ubicado la palabra
    def buscarLista(self,tipo):
        x = 0
        for x in range(len(lista)):
            if lista[x] == tipo:
                break;
            x = x + 1
        return x

    #Funcion de identificar_Token
    #Esta funcion se encarga de verificar cual es el token actual
    #Una vez que lo identifica, lo manda a buscar en la lista y devuelve la posicion donde se encuentra en la lista
    def identificar_Token(self):
        #LET
        if(self.arreglo[self.posicion].val == 'let'):
            tipo = self.buscarLista("let")
            return tipo
        #BEGIN
        elif(self.arreglo[self.posicion].val == 'begin'):
            tipo = self.buscarLista("begin")
            return tipo
        #CONST
        elif(self.arreglo[self.posicion].val == 'const'):
            tipo = self.buscarLista("const")
            return tipo
        #DO
        elif(self.arreglo[self.posicion].val == 'do'):
            tipo = self.buscarLista("do")
            return tipo
        #ELSE
        elif(self.arreglo[self.posicion].val == 'else'):
            tipo = self.buscarLista("else")
            return tipo
        #END
        elif(self.arreglo[self.posicion].val == 'end'):
            tipo = self.buscarLista("end") 
            return tipo
        #IF
        elif(self.arreglo[self.posicion].val == 'if'):
            tipo = self.buscarLista("if")
            return tipo
        #IN
        elif(self.arreglo[self.posicion].val== 'in'):
            tipo = self.buscarLista("in")
            return tipo
        #THEN
        elif(self.arreglo[self.posicion].val == 'then'):
            tipo = self.buscarLista("then")
            return tipo
        #VAR
        elif(self.arreglo[self.posicion].val == 'var'):
            tipo = self.buscarLista("var")
            return tipo
        #WHILE
        elif(self.arreglo[self.posicion].val == 'while'):
            tipo = self.buscarLista("while")
            return tipo
        #FOR
        elif(self.arreglo[self.posicion].val == 'for'):
            tipo = self.buscarLista("for")
            return tipo

        elif(self.arreglo[self.posicion].val == 'lim'):
            tipo = self.buscarLista("lim")
            return tipo
        #IDENTIFICADOR
        elif(self.arreglo[self.posicion].tipo == 'Identificador' ):
            tipo = self.buscarLista("identificador")
            return tipo
        #INTEGER
        elif(self.arreglo[self.posicion].tipo == 'Integer' ):
            tipo = self.buscarLista("int")
            return tipo
        #OPERADOR
        elif(self.arreglo[self.posicion].val in operadores):
            tipo = self.buscarLista("operador")
            return tipo
        #;
        elif (self.arreglo[self.posicion].val == ';'):
            tipo = self.buscarLista("puntoycoma")
            return tipo
        #:=
        elif (self.arreglo[self.posicion].val == ':='):
            tipo = self.buscarLista("dospuntosigual")
            return tipo
        #:
        elif (self.arreglo[self.posicion].val == ':'):
            tipo = self.buscarLista("dospuntos")
            return tipo
        #~
        elif (self.arreglo[self.posicion].val == '~'):
            tipo = self.buscarLista("rabochancho")
            return tipo
        #(
        elif (self.arreglo[self.posicion].val == '('):
            tipo = self.buscarLista("parenIzquierdo")
            return tipo
        #)
        elif (self.arreglo[self.posicion].val == ')'):
            tipo = self.buscarLista("parenDerecho")
            return tipo
        #EOT
        elif (self.arreglo[self.posicion].val == '\000'):
            tipo = self.buscarLista("eot")
            return tipo
        else:
            return
    
    
                            
    
    
            
    ##################################################################################
    """ METODOS INICIO      METODOS INICIO           METODOS INICIO """
    ##################################################################################

    #Funcion empezar_parse 
    #Esta funcion se encarga de empezar el proceso de parsing
    #Valida cuando se llego al final y imprime si hubo errores de sintaxis o no
    def empezar_parse(self):
        global arbol
        global exitoso
        self.token_Actual = self.scanAux()
        PROGRAM = self.parse_Program()
        if(self.token_Actual.token == self.buscarLista("eot")):
            print("------------------------------")
            if(exitoso == True):
                print("El proceso de analisis sintactico ha terminado con exito");
            else:
                print("El proceso de analisis sintactico tuvo errores de sintaxis")
            print("------------------------------")
        return PROGRAM    
        
def get_reportErrors():
        return reportErrors==0

def iniciar_Parser(Matriz):
    inicio = Parser(Matriz)
    print("\n------------------------------")
    print("Iniciando proceso de ANALISIS SINTACTICO....\n")
    arbol = inicio.empezar_parse()

    return arbol
