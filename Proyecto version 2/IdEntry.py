
class IdEntry:

    '''
    Clase IdEntry que va contener los componentes necesarios de cada token
    como el identificador, su atributo, y nivel(scope)
    '''
    def __init__(self, ident, declaration, level, previous):
        self.ident = ident
        self.attr = declaration
        self.level = level
        self.previous = previous
        
