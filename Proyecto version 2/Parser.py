#Parser Mini Triangulo
#TEC - Costa Rica
#Compiladores e Interpretes
#Kevin Rodriguez - Josue Rodriguez - Alejandro Salas
from AnalizadorLexico import *
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
                mensaje1="Linea : " + self.arreglo[self.posicion-1].pos
                print(mensaje1)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje1)
                    f.write('\n')

                reportErrors+=1


                mensaje2="Error de Sintáxis: El programa deberia empezar con un Single Command \n"
                print(mensaje2)
                with open('errores.txt', 'a') as f:
                   f.write(mensaje2)
                   f.write('\n')


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
                        mensaje3="Linea : " + str(self.arreglo[self.posicion-1].pos)
                        print(mensaje3)
                        with open('errores.txt', 'a') as f:
                           f.write(mensaje3)
                           f.write('\n')



                        reportErrors+=1
                        mensaje4="Error de Sintáxis: Expresion le falta Paréntesis de cierre [ ) ] \n"
                        print(mensaje4)
                        with open('errores.txt', 'a') as f:
                           f.write(mensaje4)
                           f.write('\n')




                else:
                    if(ec2 == False):
                        exitoso = False;
                        
                        mensaje5="Linea : " + str(self.arreglo[self.posicion].pos)
                        print(mensaje5)
                        with open('errores.txt', 'a') as f:
                           f.write(mensaje5)
                           f.write('\n')




                        reportErrors+=1
                        mensaje6="Error de Sintaxis: Assign Command le falta [ := ]" + "en lugar de: " + str(self.arreglo[self.posicion].val) + " \n"
                        print(mensaje6)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje6)
                            f.write('\n')

                        




                        return False;
                    else:
                        exitoso = False;

                        mensaje7="Linea : " + str( self.arreglo[self.posicion].pos)
                        print(mensaje7)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje7)
                            f.write('\n')



                        reportErrors+=1
                        mensaje8="Error de Sintáxis: Expresion le falta Paréntesis de inicio [ ( ] \n"
                        print(mensaje8)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje8)
                            f.write('\n')



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
                    mensaje9="Linea : " + str(self.arreglo[self.posicion].pos)
                    print(mensaje9)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje9)
                        f.write('\n')



                    reportErrors+=1
                    mensaje10="Error de Sintáxis : If le falta la palabra reservada [ then ] \n"
                    print(mensaje10)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje10)
                        f.write('\n')


                COMMAND = self.parse_Single_Command()
                if(self.token_Actual.token == self.buscarLista("else")):
                    self.aceptarToken()
                else:
                    exitoso = False;
                    mensaje11="Linea : " + str(self.arreglo[self.posicion].pos)
                    print(mensaje11)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje11)
                        f.write('\n')


                    reportErrors+=1
                    mensaje12="Error de Sintáxis : If le falta la palabra reservada [ else ] \n"
                    print(mensaje12)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje12)
                        f.write('\n')


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
                    mensaje13= "Linea : " + str(b)
                    print(mensaje13)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje13)
                        f.write('\n')


                    reportErrors+=1
                    mensaje14="Error de Sintáxis: While le falta la palabra reservada [ do ] \n"
                    print(mensaje14)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje14)
                        f.write('\n')



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
                        mensaje15="Linea : " + str(self.arreglo[self.posicion].pos)
                        print(mensaje15)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje15)
                            f.write('\n')




                        reportErrors+=1
                        mensaje16="Error de Sintáxis: For le falta la palabra reservada [lim] \n"
                        print(mensaje16)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje16)
                            f.write('\n')


                else:
                    exitoso = False;
                    mensaje17="Linea : " + str(self.arreglo[self.posicion].pos)
                    print(mensaje17)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje17)
                        f.write('\n')


                    reportErrors+=1
                    mensaje18="Error de Sintáxis: For le falta la palabra reservada [ in ]  \n"
                    print(mensaje18)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje18)
                        f.write('\n')



          
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
                    mensaje19="Linea : " + str(b)
                    print(mensaje19)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje19)
                        f.write('\n')



                    reportErrors+=1
                    mensaje20="Error de Sintáxis: let le falta la palabra reservada [ in ] \n"
                    print(mensaje20)
                    with open('errores.txt', 'a') as f:
                        f.write(mensaje20)
                        f.write('\n')





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
                        mensaje21="Linea : " + str(b)
                        print(mensaje21)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje21)
                            f.write('\n')


                        reportErrors+=1
                        mensaje22="Error de Sintáxis: Begin deberia terminar con la palabra reservada [ end ] \n"
                        print(mensaje22)
                        with open('errores.txt', 'a') as f:
                            f.write(mensaje22)
                            f.write('\n')


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
                mensaje23="Linea : " + str(self.arreglo[self.posicion-1].pos)
                print(mensaje23)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje23)
                    f.write('\n')
                


                reportErrors+=1
                mensaje24="Error de Sintáxis: Expresion le falta Paréntesis de cierre [ ) ] \n"
                print(mensaje24)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje24)
                    f.write('\n')

        else:
            exitoso = False;
            self.token_Actual = self.scannear()
            b = self.arreglo[self.posicion-1].pos
            b = int(b) + 0
            mensaje25="Linea : " + str(b)
            print(mensaje25)
            with open('errores.txt', 'a') as f:
                f.write(mensaje25)
                f.write('\n')


            reportErrors+=1
            mensaje26="Error de Sintáxis: Expresion es invalida, no cumple con ser Identificador, Integer , Operador Expresion o ( EXpresion ) \n"
            print(mensaje26)
            with open('errores.txt', 'a') as f:
                f.write(mensaje26)
                f.write('\n')




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
                mensaje27="Linea : " + str(self.arreglo[self.posicion].pos)
                print(mensaje27)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje27)
                    f.write('\n')

                reportErrors+=1
                mensaje28="Error de Sintáxis: Declaracion le falta [ ; ] \n"
                print(mensaje28)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje28)
                    f.write('\n')



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
                     mensaje29="Linea : " + str(b)
                     print(mensaje29)
                     with open('errores.txt', 'a') as f:
                        f.write(mensaje29)
                        f.write('\n')



                     reportErrors+=1
                     mensaje30="Error de Sintaxis: Quitar el simbolo [;] \n"
                     print(mensaje30)
                     with open('errores.txt', 'a') as f:
                         f.write(mensaje30)
                         f.write('\n')



                 else:
                     exitoso = False;
                     mensaje31="Linea : " + str(self.arreglo[self.posicion].pos)
                     print(mensaje31)
                     with open('errores.txt', 'a') as f:
                         f.write(mensaje31)
                         f.write('\n')




                     reportErrors+=1
                     mensaje32="Error de Sintáxis: Despues [ let ] deberia seguir un Single Declaration [ const ] o [ var ] \n"
                     print(mensaje32)
                     with open('errores.txt', 'a') as f:
                         f.write(mensaje32)
                         f.write('\n')




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
                mensaje33="Linea : " + str(self.arreglo[self.posicion].pos)
                print(mensaje33)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje33)
                    f.write('\n')


                reportErrors+=1
                mensaje34="Error de Sintáxis: Despues [ let ] deberia seguir un Single Declaration [ const ] o [ var ] \n"
                print(mensaje34)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje34)
                    f.write('\n')


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
                mensaje35="Linea : " + str(b)
                print(mensaje35)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje35)
                    f.write('\n')



                reportErrors+=1
                mensaje36="Error de Sintaxis: [ var ] Tiene que terminar con un Type-denoter [ Identificador ] que sea valido \n"
                print(mensaje36)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje36)
                    f.write('\n')


            else:
                exitoso = False;
                mensaje37="Linea : " + str(self.arreglo[self.posicion].pos)
                print(mensaje37)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje37)
                    f.write('\n')


                reportErrors+=1
                mensaje38="Error de Sintáxis: Identificador invalido \n"
                print(mensaje38)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje38)
                    f.write('\n')



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
            mensaje39="Linea : " + str(self.arreglo[self.posicion].pos)
            print(mensaje39)
            with open('errores.txt', 'a') as f:
                f.write(mensaje39)
                f.write('\n')



            reportErrors+=1
            mensaje40="Error de Sintáxis: No es un integer \n"
            print(mensaje40)
            with open('errores.txt', 'a') as f:
                f.write(mensaje40)
                f.write('\n')



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
            mensaje41="Linea : " + self.arreglo[self.posicion].pos
            print(mensaje41)
            with open('errores.txt', 'a') as f:
                f.write(mensaje41)
                f.write('\n')


            reportErrors+=1
            mensaje42="Error de Sintáxis: No es un operador \n"
            print(mensaje42)
            with open('errores.txt', 'a') as f:
                f.write(mensaje42)
                f.write('\n')





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
                mensaje43="Linea : " + str(self.arreglo[self.posicion].pos)
                print(mensaje43)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje43)
                    f.write('\n')


                reportErrors+=1
                mensaje44="Error de Sintaxis: Esperaba el simbolo [ ~ ] antes de la expresion para [ const ] \n"
                print(mensaje44)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje44)
                    f.write('\n')



                exitoso = False
                self.token_Actual = self.scannear()
            elif((esperado ==  self.buscarLista("dospuntos"))):
                mensaje45="Linea : " + str(self.arreglo[self.posicion].pos)
                print(mensaje45)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje45)
                    f.write('\n')



                reportErrors+=1
                mensaje46="Error de Sintaxis: Esperaba el simbolo [ : ] antes del identificador para [ var ] \n"
                print(mensaje46)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje46)
                    f.write('\n')


                exitoso = False;
                self.token_Actual = self.scannear()
            else:
                 mensaje47="ERROR"
                 print(mensaje47)
                 with open('errores.txt', 'a') as f:
                   f.write(mensaje47)
                   f.write('\n')

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
                mensaje48="El proceso de analisis sintactico ha terminado con exito"
                print(mensaje48)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje48)
                    f.write('\n')
            else:
                mensaje49="El proceso de analisis sintactico tuvo errores de sintaxis"
                print(mensaje49)
                with open('errores.txt', 'a') as f:
                    f.write(mensaje49)
                    f.write('\n')
            mensaje50="==========================================================="
            print(mensaje50)
            with open('errores.txt', 'a') as f:
                f.write(mensaje50)
                f.write('\n')
        return PROGRAM    
        
def get_reportErrors():
        return reportErrors==0

def iniciar_Parser(Matriz):
    inicio = Parser(Matriz)
    print("\n------------------------------")
    mensaje51="  ========================== IniciandoANALISIS SINTACTICO ==========================\n"
    print(mensaje51)
    with open('errores.txt', 'a') as f:
        f.write(mensaje51)
        f.write('\n')
    arbol = inicio.empezar_parse()

    return arbol
