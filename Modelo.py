# -*- coding: utf-8 -*-
"""
@author: Laura Berrio Velez, Maria Paulina Salazar Meneses
trabajo 2_Bioseñales
"""
#EN ESTE CODIGO SE REALIZAN TODAS LAS ACCIONES DEL PROBLEMA
##funciones similares en el modelo estan en el controlador con igual nombre
# SE EJECUTAN LAS OPERACIONES BÁSICAS SOBRE LA SEÑAL, COMO DESPLAZARLA, DESCOMPONERLA, FILTRARLA, ENTRE OTRAS

import numpy as np  # Librería de manejo de arreglos de grandes dimensiones
import matplotlib.pyplot as plt;
import scipy.io as sio;
#from chronux.mtspectrumc import mtspectrum

#library to load mat files
import scipy.io as sio;
import matplotlib.pyplot as plt;
import numpy as np;
import scipy.signal as signal;





class Biosenal(object):  # Se crea la clase Biosenal en Modelo
 # La clase Biosenal manipula un nuevo array para poder obtener segmentos del mismo   
    def __init__(self,data=None):
        if not data==None:
            self.asignarDatos(data)
        else:
            self.__data=np.asarray([])
            self.__canales=0
            self.__puntos=0# Este modelo tendrá un nuevo array con sus respectivos canales y puntos       
            
    def asignarDatos(self,data):  
        self.__data=data
        self.__canales= 1
        self.__puntos=data.shape[0]
        
        
       
    
    def devolver_segmento(self,x_min,x_max):  # Con ese nuevo array puede volverse un segmento de la señal mediante el xlim de numpy
        #prevengo errores logicos
        if x_min>=x_max:  # No se devuelve ningun segmento si x min es mayor o igual a xmax, puesto que se piden mas cosas de las que existen
            return None
       
        return self.__data[x_min:x_max]   # Se extraen los valores que se necesitan en la biosenal
    
    
    # permite devolver el canal con los xlim del sistema  (limites)
    
    def calcularWavelet(self,senal):
        
        
        #%%analisis usando wavelet continuo
        import pywt #1.1.1

        #%%
        sampling_period =  1/1000
        Frequency_Band = [4, 30] # Banda de frecuencia a analizar
        
        # Métodos de obtener las escalas para el Complex Morlet Wavelet  
        # Método 1:
        # Determinar las frecuencias respectivas para una escalas definidas
        scales = np.arange(1, 250)
        frequencies = pywt.scale2frequency('cmor', scales)/sampling_period
        # Extraer las escalas correspondientes a la banda de frecuencia a analizar
        scales = scales[(frequencies >= Frequency_Band[0]) & (frequencies <= Frequency_Band[1])]
        
        N = senal.shape[0]
        #%%
        # Obtener el tiempo correspondiente a una epoca de la señal (en segundos)
        time_epoch = sampling_period*N

        # Analizar una epoca de un montaje (con las escalas del método 1)
        # Obtener el vector de tiempo adecuado para una epoca de un montaje de la señal
        time = np.arange(0, time_epoch, sampling_period)
        # Para la primera epoca del segundo montaje calcular la transformada continua de Wavelet, usando Complex Morlet Wavelet

        [coef, freqs] = pywt.cwt(senal, scales, 'cmor', sampling_period)
        # Calcular la potencia 
        power = (np.abs(coef)) ** 2
        
        return time, freqs, power
        
        
    def calcularWelch(self,senal):
        pass
    def calcularMultitaper(self,senal):
        pass
   
    
