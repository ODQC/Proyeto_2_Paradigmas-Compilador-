
import io
import string
import sys

Lista = []
Matriz=[]
reportErrors=0


#************************************************************************
'''Declaracion de variables'''

TOKENS = ['Identificador', 'Integer', 'Operador','BEGIN',
          'CONST', 'DO',  'ELSE', 'END', 'IF', 'IN', 'LET',  'THEN', 'VAR', 'WHILE',
          'Simbolo','EOT', 'FUNC', 'RETURN','PalabraReservada','Error','FOR','LIM']

Operadores = ['+', '-','*','/','<','>','=','\\']
PalabrasReservadas = {'begin': 3, 'const' :4, 'do':5, 'else':6, 'end'  : 7, 'if' :8, 'in':9, 'let':10, 'then':11, 'var': 12, 'while': 13, 'func' :16, 'return': 17,'for':18,'lim':19}

#**********************************************************************

class Token(object):
    """ A simple Token structure.
        
        Contains the token type, value and position. 
    """
    def __init__(self, tipo, val, pos):
        self.tipo = TOKENS[tipo]
        self.val = val
        self.pos = pos
        self.scope=-1

    def __str__(self):
        return '(%s(%s) at %s)' % (self.tipo, self.val, self.pos)

    def __repr__(self):
        return self.__str__()



class ScannerError(Exception):
    """ Se le muestra el error al usuario se recibe la linea
        el simbolo o palabra por la cual dio error
    """
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char

    def __str__(self):
        return 'Imprimiendo Tipo Error  Imprimiento en linea= %d,  Imprimiendo  dato:   %s \n' % (self.pos, self.char)
#**********************************************************************
    
class Scanner():
    """Clase en la cual se detecta si un caracter es valido o incorrecto
        con respecto al lenguaje minitriangulo

    """
#**********************************************************************
    def __init__(self, texto,x):
        ''''Se recibe la linea a leer y el numero de linea que es
            se convierte la linea a ioSTRING para usar el metodo read
            se tiene un booleano para saber si ya se ha llegado al final de la
            linea y un caracter para saber cual se esta leyendo actualmente'''
        self.linea=x
        self.archivo = io.StringIO(texto)
        self.fin_Linea = False   
        self.caracter = ''

        self.actualizar_Caracter()   
#**********************************************************************
    def scan(self):
        """Funcion en la cual se recorre cada linea del archivo de texto
            en caso de ser un token valido se almacena en la lista 
        """
        
        while 1:
            token = self.scan_token()
            
            if token == 0:
                break
            Lista.append(token)
     

  
  #**********************************************************************  
    def scan_token(self): 
        """Se recorre caracter por caracter cuando se encuentre un identificador
            o digito se comienza almacenando los demas si son del mismo tipo o letras
            siempre y cuando sen validos luego se retorna el token valido, en caso de ser espacio
            se ignora y se continua igual que los comentarios."""
        global reportErrors
        actual = self.caracter
        token = 0
        
        while not self.fin_Linea:
            
            if actual.isspace():
                self.actualizar_Caracter()
                actual = self.caracter
                continue
            elif actual == '!':
                self.actualizar_Caracter()

                while self.caracter != '\n' and not self.fin_Linea:
                    self.actualizar_Caracter() #cuando comienza un comentario comienza tomando los caracteres ignorandolos
                self.actualizar_Caracter() #al llegar al fin coloca el bolean en true indicando que ya finalizo la linea y asi hacer el break
                actual = self.caracter
                continue
            
            elif actual.isdigit() :
                token = self.scan_int()
                break
            elif actual.isalpha():
                token = self.scan_ident()                   
                break
            elif actual == ';':
                
                token= Token(14, ';', self.linea)
            
                self.actualizar_Caracter()
                break
            elif actual == ',':
             
                token  = Token(14, ',', self.linea)
                self.actualizar_Caracter()
                break
            elif actual == ':':  
                 
                self.actualizar_Caracter()
                token = self.verificar_Igual()# verifica si luego de dos puntos existe un igual
                
                break
            elif actual == '~':
                
                token = Token(14, '~', self.linea)
                self.actualizar_Caracter()
                break
            elif actual in Operadores:
                
                token = Token(2, actual, self.linea)
                self.actualizar_Caracter()
                break
            elif actual == '(':
               
                token = Token(14, '(', self.linea)
                self.actualizar_Caracter()
                break
            elif actual == ')':
               
                token = Token(14, ')', self.linea)
                self.actualizar_Caracter()
                break
            else:
                reportErrors+=1
                raise ScannerError(self.linea,  self.caracter)

        return token
           
        
           
  #**********************************************************************      
    def verificar_Igual(self):
        '''Funcion en la cual se verifica si el caracter siguiente a : es un igual o no'''
        
        if self.caracter == '=':
           
            token = Token(14, ':=', self.linea)
            self.actualizar_Caracter()
            return token
        else:
            token = Token(14, ':', self.linea)
            return token
          
    
#**********************************************************************    
    def scan_int(self):
        """Funcion en la cual se verifica si el siguiente caracter a leer es int
            en caso de serlo lo almacena en  una lista luego lo concatena
            y se crea un objeto token con el tipo int, si luego del digito int sigue
            un alpha se toma como error ejemplo '333alguna cosa'"""
   
        
        lista = [self.caracter]    #mete el primer numero del INT A LA LISTA       
        self.actualizar_Caracter()
    
        while self.caracter.isdigit() :
            lista.append(self.actualizar_Caracter())

        if not self.caracter.isalpha():
           
            return Token(1, int(''.join(lista)), self.linea)
            #return token

        while self.caracter.isalnum()    :
            lista.append(self.caracter)
            self.actualizar_Caracter()

        string_Lista = ''.join(lista)
        return Token(19, string_Lista, self.linea)

  #**********************************************************************  
    def scan_ident(self):
        """Funcion en la cual se detecta si el primer caracter es una letra
            en caso de que si se procede a seguir almacenando caracteres digitos
            o letras en una variable para luego retornar un identificador valido, se detiene
            hasta cuando ya no sea ni letra ni numero"""
    
        lista = [self.actualizar_Caracter()]
        
        while self.caracter.isalnum():
            lista.append(self.actualizar_Caracter())
            
        string_Lista = ''.join(lista)
        
        if string_Lista in PalabrasReservadas:
           
             return  Token(18, string_Lista, self.linea)
      
        
        return Token(0, string_Lista, self.linea)

#**********************************************************************
    def actualizar_Caracter(self):
        """Funcion en la cual se actualiza el caracter actual que se esta leyendo
            ademas se verifica si ya ha llegado al final de la linea, para ello se usa el
            metodo read de la libreria io en python 3
        """

        temporal = self.caracter
        
        self.caracter = self.archivo.read(1)
        if self.caracter == '':  #fin de linea
            
            self.fin_Linea = True

        return temporal
        


    
#**********************************************************************

 #**********************************************************************
def verificar_Scanner(archivo):
    ''' Metodo main en el cual se lee linea a linea el archivo de texto plano'''
    
    exprs = archivo 
    x=1 #indica el numero de linea
    lista=[]
    for exp in exprs:
        scanner = Scanner(exp,x)
        x+=1
            
           
        try:
            scanner.scan()
            
        except ScannerError as e:
            mensaje=e
            print (mensaje)
            with open('errores.txt', 'a') as f:
                f.write(mensaje)
                f.write('\n')

   
    return Lista
        
    
#########################################
def getReportErrors():
    return reportErrors
