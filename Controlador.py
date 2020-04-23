# ESTE CODIGO CORRESPONDIENTE AL CONTROLADOR ES EL QUE PERMITE QUE LAS CLASES MODELO, INTERFAZ Y  CONTROLADOR FUNCIONEN EN CONJUNTO
# AQUI LO QUE PIDE LA INTERFAZ SE LE PASA AL MODELO

"""
trabajo dos Bioseñales
@author: Maria Paulina Salazar Meneses y Laura  Berrio Velez
"""
from Modelo import Biosenal  # Se importa la clase Biosenal del archivo Modelo
from interfaz import Interfaz  # Se importa la clase interfaz del archivo llamado interfaz
import sys  # # Librería que proporciona parámetros y funciones específicas del sistema
from PyQt5.QtWidgets import QApplication  
# Se importa el módulo QApplication para pueda funcionar todos los programas relacionados con la interfaz
#library to load mat files
import scipy.io as sio;
import matplotlib.pyplot as plt;
import numpy as np;




class Principal(object): 
    def __init__(self):        
        self.__app=QApplication(sys.argv)
        self.__mi_vista=Interfaz()  # se accede a los atributos de la clase Interfaz
        self.__mi_biosenal=Biosenal()  # se accede a los atributos de la clase Biosenal
        self.__mi_controlador=Coordinador(self.__mi_vista,self.__mi_biosenal)  # Se le asigna al coordinador la vista y biosenal
        self.__mi_vista.asignar_Controlador(self.__mi_controlador)  #  Se le asigna al controlador la vista 
    def main(self):
        self.__mi_vista.show() # Permite mostrar las ventanas 
        sys.exit(self.__app.exec_()) #Permite ejecutar la aplicación 
    
class Coordinador(object):
# La clase coordinador accede a los objetos de la vista y el modelo (biosenal), ya que su función es permitir
#que la vista y el modelo funcionen en conjunto
    def __init__(self,vista,biosenal): 
        self.__mi_vista=vista
        self.__mi_biosenal=biosenal
        
    def recibirDatosSenal(self,data):  # Esta función permite asignarle los datos de la señal continua al Modelo 
        self.__mi_biosenal.asignarDatos(data)
    

    def devolverDatosSenal(self,x_min,x_max):  # Esta función permite devolver un segmento de acuerdo a los valores mínimos y máximos
        return self.__mi_biosenal.devolver_segmento(x_min,x_max)

    
    def calcularWavelet(self,data,fs):
        return self.__mi_biosenal.calcularWavelet(data,fs)
    
    def calcularWelch(self,data,fm,ta,so,po):
        return self.__mi_biosenal.calcularWelch(data,fm,ta,so,po)
        
        
    def calcularmulti(self,data,fmp,ab,tam):
        return self.__mi_biosenal.calcularMultitaper(data,fmp,ab,tam)
    
    
    
p=Principal()
p.main()