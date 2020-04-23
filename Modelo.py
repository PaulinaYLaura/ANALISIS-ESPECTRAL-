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
            
    def asignarDatos(self,data):  #en este caso la señal que usamos  solo tiene un canal
        self.__data=data
        self.__canales= 1
        self.__puntos=data.shape[0]
        
        
       
    
    def devolver_segmento(self,x_min,x_max):  # Con ese nuevo array puede volverse un segmento de la señal mediante el xlim de numpy
        #prevengo errores logicos
        if x_min>=x_max:  # No se devuelve ningun segmento si x min es mayor o igual a xmax, puesto que se piden mas cosas de las que existen
            return None
       
        return self.__data[x_min:x_max]   # Se extraen los valores que se necesitan en la biosenal
    
    
    # permite devolver el canal con los xlim del sistema  (limites)
    
    def calcularWavelet(self,data,fs): #funcion que realiza todo el proceso de analisis espectral por wavelet
        
        senal =self.__data[:]
        sen= senal - np.mean(senal)
        
        
        
        import pywt #se importa la libreria

        
        sampling_period =  1/fs
        Frequency_Band = [4, 30] # Banda de frecuencia a analizar
        
        # Métodos de obtener las escalas para el Complex Morlet Wavelet  
        # Método 1:
        # Determinar las frecuencias respectivas para una escalas definidas
        scales = np.arange(1, 250)
        frequencies = pywt.scale2frequency('cmor', scales)/sampling_period
        # Extraer las escalas correspondientes a la banda de frecuencia a analizar
        scales = scales[(frequencies >= Frequency_Band[0]) & (frequencies <= Frequency_Band[1])]
        
        N = sen.shape[0]
        
        # Obtener el tiempo correspondiente a una epoca de la señal (en segundos)
        time_epoch = sampling_period*N

        # Analizar una epoca de un montaje (con las escalas del método 1)
        # Obtener el vector de tiempo adecuado para una epoca de un montaje de la señal
        time = np.arange(0, time_epoch, sampling_period)
        # Para la primera epoca del segundo montaje calcular la transformada continua de Wavelet, usando Complex Morlet Wavelet

        [coef, freqs] = pywt.cwt(sen, scales, 'cmor', sampling_period)
        # Calcular la potencia 
        power = (np.abs(coef)) ** 2
        
        return time, freqs, power
#%%analisis usando multitaper        
        
    def calcularWelch(self,data,fm,ta,so,po): #funcion para ejecutar el codigo del welch sobre la señal
        
        data = self.__data[:]
        sen = data-np.mean(data)
        
        f, Pxx = signal.welch(sen,fm,'hamming', ta, so, po, scaling='density');# welch
        return f, Pxx #devolver los datos necesarios para graficarla
        
        

    def calcularMultitaper(self,data,fmp,ab,tam,inicial,final): #funcion para ejecutar el codigo del multitaper
        
        data =self.__data[:]
        
        sen= data - np.mean(data)
        
        from chronux.mtspectrumc import mtspectrumc # se importa la liberia necesaria para su ejecucion
        
        params = dict(fmp = fmp, fpass = [inicial, final], tapers = [ab, tam, 1], trialave = 1) # en esta variable queda los datos del multitaper

        data = np.reshape(sen,(fmp*5,10),order='F') #esta variable reliza un redimension de los datos

#Calculate the spectral power of the data
        Pxx, f = mtspectrumc(data, params) # se gurada en esta variables los datos resultado del mtspectrum 
        #A numeric vector [W T p] where W is the
        #bandwidth, T is the duration of the data and p 
        #is an integer such that 2TW-p tapers are used.
        return Pxx, f # se envian para ser graficados o utilizados donde se llamen
        
   
