class Type():

    '''
    Constructor de type con el atributo tipo
    '''
    def __init__(self, tipo):
      self.type = tipo 

    '''
    Funcion que compara dos tipos y retorna true si son iguales y false sino lo son
    '''
    def equals(self, other):
        if(self.type==other.type):
            return True
        return False

    '''
    Funcion que obtiene el nombre de la clase y lo retorna
    '''
    def getName(self):
        return self.__class__.__name__
       
