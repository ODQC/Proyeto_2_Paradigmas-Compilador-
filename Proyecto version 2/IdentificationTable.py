#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
class IdentificationTable(object):
    '''
    Funcion que inicializa la tabla de simbolos y tiene como atributos tabla y scope
    '''
    def __init__(self):
      self.tabla={}
      self.scope=0

    '''
    Verifica si un objeto ya esta en el diccionario o no, recibe llave valor y si
    esta el elemento retorna true sino false
    '''
    def verificarExistencia(self,identificador):
        try:
            encontrado = self.tabla[identificador,self.scope]
            return True
        except:
    
            return False

    '''
    
    '''
    def verificarAmbienteEstandar(self,identificador):
        try:
            encontrado = self.tabla[identificador,0]
            return True
        except:
    
            return False

    '''
    Verifica el tipo de un objeto que se encuentra en la tabla
    '''
    def verificarTipo(self,identificador):
        elemento=self.tabla[identificador,self.scope]
        

    '''
    Cuando encuentra un let aumenta el nivel 
    '''
    def openScope(self):
        self.scope+=1

    '''
    Cuando encuentra un let disminuye el nivel 
    '''
    def closeScope(self):
        self.scope-=1


    '''
    Obtiene el objeto existente mediante un identificador y lo retorna 
    '''
    def obtenerExistente(self,identificador):
        try:
            existente=tabla.tabla[self.identificador,tabla.scope]
        except:
            return False
        return existente


    '''
    Inserta el atributo en la tabla 
    '''
    def enter(self,llave,atributo):
        try:
            encontrado = self.tabla[llave,self.scope]
            return False
        except:
    
            self.tabla[llave,self.scope] = atributo
            return True
    
        
