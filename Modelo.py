# -*- coding: utf-8 -*-
"""
@author: Laura Berrio Velez, Maria Paulina Salazar Meneses
"""
#EN ESTE CODIGO SE REALIZAN TODAS LAS ACCIONES DEL PROBLEMA
##funciones similares en el modelo estan en el controlador con igual nombre
# SE EJECUTAN LAS OPERACIONES BÁSICAS SOBRE LA SEÑAL, COMO DESPLAZARLA, DESCOMPONERLA, FILTRARLA, ENTRE OTRAS

import numpy as np  # Librería de manejo de arreglos de grandes dimensiones
import matplotlib.pyplot as plt;
import scipy.io as sio;

wavelet = [-1/np.sqrt(2) , 1/np.sqrt(2)];
scale = [1/np.sqrt(2) , 1/np.sqrt(2)];

wavelet_inv = [1/np.sqrt(2) , -1/np.sqrt(2)];
scale_inv = [1/np.sqrt(2) , 1/np.sqrt(2)];


class Biosenal(object):  # Se crea la clase Biosenal en Modelo
 # La clase Biosenal manipula un nuevo array para poder obtener segmentos del mismo   
    def __init__(self,data=None):
        if not data==None:
            self.asignarDatos(data)
        else:
            self.__data=np.asarray([])    # Este modelo tendrá un nuevo array con sus respectivos canales y puntos
            self.__canales=0
            self.__puntos=0
            
    def asignarDatos(self,data):  
        self.__data=data
        self.__canales=data.shape[0]
        self.__puntos=data.shape[1]
    
    def devolver_segmento(self,x_min,x_max):  # Con ese nuevo array puede volverse un segmento de la señal mediante el xlim de numpy
        #prevengo errores logicos
        if x_min>=x_max:  # No se devuelve ningun segmento si x min es mayor o igual a xmax, puesto que se piden mas cosas de las que existen
            return None
       
        return self.__data[:,x_min:x_max]   # Se extraen los valores que se necesitan en la biosenal
    
    def devolver_canal(self,canal, x_min, x_max):
        if (x_min >= x_max) and (canal > self.__canales):
            return None
        return self.__data[canal,x_min:x_max]  # permite devolver el canal con los xlim del sistema  (limites)
    
    def ventanas(self,data):
        pass
    
