
"""Trabajo numero 2 analisis Espectral Bioseñales
autores: Laura Marcela Berrio, Maria Paulina Salazar Meneses"""




# EN ESTE CODIGO SE INCLUYE TODO LO QUE ESTE RELACIONADO CON LA INFORMACION QUE SE RECIBE Y SE LE DA AL USUARIO 
import sys # Librería que proporciona parámetros y funciones específicas del sistema
#Qfiledialog es una ventana para abrir y guardar archivos
#Qvbox es un organizador de widget en la ventana, este en particular los apila en vertical
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from PyQt5 import QtCore, QtWidgets

from matplotlib.figure import Figure

from PyQt5.uic import loadUi  #Permite cargar lo que se desarrolle en el Designer 
from PyQt5.QtGui import QIntValidator

from numpy import arange, sin, pi 
# De la librería de numpy se importa la función arange para crear arrays, la función seno y el número pi (3.1416)

#contenido para graficos de matplotlib
from matplotlib.backends. backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import scipy.io as sio  # Librería científica que soporta la carga de multiples tipos de archivos
import numpy as np # librería que permite trabajar con arrays
import matplotlib.pyplot as plt;
import scipy.signal as signal;

from Modelo import Biosenal # Del archivo Modelo se importa la
from scipy.fftpack import fft;

#from chronux.mtspectrumc import mtspectrumc






# Se utilizo esta clase para graficar ya que la version de Qt de nuestros pcs no permitieron graficar con una ventana Qview por la
#componente pyqtgraphs que no permitio ejecutar la interfaz
class MyGraphCanvas(FigureCanvas):
    #constructor
    def __init__(self, parent= None,width=5, height=4, dpi=100):
        
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #self.fig2= Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axes = self.fig.add_subplot(111)
        
        
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    def __init2__(self, parent= None,width=5, height=4, dpi=100):
        
        #se crea un objeto figura
        self.fig2 = Figure(figsize=(width, height), dpi=dpi)
        #self.fig2= Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        
        self.axes2 = self.fig2.add_subplot(121)
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init2__(self,self.fig2)
        
    
        
#Se ingresan los datos a graficar y se grafican

  
 #cuando se utiliza plot las señales quedan en la misma gráfica
 
    # Se crea un metodo para graficar lo que se desee
        
    def graficar_senal(self,datos): # funcion en la interfaz para graficar la se�al cargada
        self.axes.clear()
        #Se ingresan los datos a graficar y se grafican
        self.axes.plot(datos) 
        print("datos")
        print(datos)
   
        self.axes.set_xlabel("Muestras") # Al eje x se le asigna el nombre muestras
        self.axes.set_ylabel("Amplitud") # Al eje y se le asigna el nombre amplitud
        #self.axes.set
        
        self.axes.figure.canvas.draw() # Se da la indidicación de que se dibuje la figura
        
        
        
        
    def graficar_espectro(self,time, freqs, power): # la funcion para graficar el espectro del wavelet
        self.axes.clear() # se limpia el espacio antes de graficar
        self.axes.contourf(time,
                 freqs[(freqs >= 4) & (freqs <= 40)], #anchos de frecuencias en los cuales se va a analizar
                 power[(freqs >= 4) & (freqs <= 40),:],
                 20, # Especificar 20 divisiones en las escalas de color 
                 extend='both')
        print("datos")
        self.axes.set_ylabel('frequency [Hz]') #nombre de los ejes
        self.axes.set_xlabel('Time [s]')
        self.axes.figure.canvas.draw()#ordenamos que dibuje
        
    def graficar_analisisw(self,f,Pxx): #esta funcion recibe los datos del modelo para graficar el welch
        self.axes.clear()
        self.axes.plot(f[(f >= 4) & (f <= 40)],Pxx[(f >= 4) & (f <= 40)]) # rango de frecuencias a analizar 
        self.axes.set_xlabel('frequency [Hz]')
        
        self.axes.figure.canvas.draw()#ordenamos que dibuje
        
    def graficar_analisisp(self,Pxx,f): # esta funcion recibe del modelo los datos para graficar por el metodo multitaper
        self.axes.clear()
        self.axes.plot(f[(f >= 4) & (f <= 40)],Pxx[(f >= 4) & (f <= 40)]) # rango de frecuencias a analizar
        self.axes.set_xlabel('frequency [Hz]')
        
        self.axes.figure.canvas.draw() # se ordena que grafique

#signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, 
#detrend='constant', return_onesided=True, scaling='density', axis=-1)
#f, Pxx = signal.welch(ecg,fs,'hamming', 512*0.5, 256*0.5, 512*0.5, scaling='density');

   
    
        
#la siguiente clase se encarga de todos los comandos instituidos en la interfaz grafica                 
       
class Interfaz(QMainWindow): # Clase que se define para crear las interfaces gráficas, ventana principal
    #constructor
    def __init__(self): 
        #siempre va
        super(Interfaz,self).__init__() # Se llama al constructor de la clase principal
        #se carga el diseño
        loadUi ('ventana_senal2.ui',self)
        #se llama la rutina donde configuramos la interfaz
        self.setup()
        #se muestra la interfaz
        self.show()
    def setup(self):
        #los layout permiten organizar widgets en un contenedor
        #esta clase permite añadir widget uno encima del otro (vertical)
        layout = QVBoxLayout()
        layout2 = QVBoxLayout()
        
        #se añade el organizador al campo grafico
        self.campo_graficacion.setLayout(layout)
        self.campo_w.setLayout(layout2)
        
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_graficacion, width=5, height=4, dpi=100) # para el primer grafico
        self.__sc2 = MyGraphCanvas(self.campo_w, width=5, height=4, dpi=100) #
        
        
        
        #se añade el campo de graficos
        layout.addWidget(self.__sc)
        layout2.addWidget(self.__sc2)
        
        
        #se organizan las señales 
        self.boton_cargarsenal.clicked.connect(self.cargar_senal)  # El usuario puede dar click sobre el botón para cargar la señal
        #El botón desplazamiento en el tiempo tiene la opción de adelantar o atrasar la señal cargada
        self.boton_adelante.clicked.connect(self.adelante_senal) 
        self.boton_atras.clicked.connect(self.atrasar_senal)
        self.boton_wavelet.clicked.connect(self.wavelet)
        self.boton_gr.clicked.connect(self.welch)
        self.boton_mp.clicked.connect(self.multitaper)
        
        # El usuario puede escribir el número del canal que desee visualizar y da clic en seleccionar canal
        #self.seleccion_canal.clicked.connect(self.graficar_canal) 
        #self.campo.setValidator(QIntValidator(0,10))  # Se asigna un QInt Validator para que se tomen canales entre 0 y 10
         
 #Los botones adelantar y atrasar señal asociados al desplazamiento de la señal no se habilitan si la señal no esta cargada
        self.boton_adelante.setEnabled(True)
        self.boton_atras.setEnabled(True)
        
        # El botón seleccionar canal no esta disponible si el usuario no ha cargado la señal
          # La función QFileDialog muestra el cuadro de diálogo para seleccionar la señal que se quiere cargar 
        
        #los botones, checkbox y combobox para el analisis espectral
        self.checkWelch.stateChanged.connect(self.cambio)
        self.checkMulti.stateChanged.connect(self.cambio)
       
        self.tipo_ventana.addItem("hamming")
        
    
        
    
    def cambio(self):# funcion para habilitar los botones check en la interfaz para el welch y para el multitaper
        
        if self.checkWelch.isChecked() == True:
            
            self.checkMulti.setEnabled(False) #por orden y evitar seleccionar las dos opciones al tiempo
            self.fs_multi.setEnabled(False)
            self.we.setEnabled(False)
            self.tama.setEnabled(False)
            self.ini.setEnabled(False)
            self.fin.setEnabled(False)
           
        
        if self.checkMulti.isChecked() == True: #por orden y evitar seleccionar las dos opciones al tiempo
            
            self.checkWelch.setEnabled(False)
            self.tipo_ventana.setEnabled(False)
            self.tamano.setEnabled(False)
            self.solapamiento.setEnabled(False)
            self.frecuencia_w.setEnabled(False)
            self.potencia.setEnabled(False)
            
        if self.checkWelch.isChecked() == False:#por orden y evitar seleccionar las dos opciones al tiempo
            
            self.checkMulti.setEnabled(True)
            self.fs_multi.setEnabled(True)
            self.we.setEnabled(True)
            self.tama.setEnabled(True)
            self.ini.setEnabled(True)
            self.fin.setEnabled(True)
            
        if self.checkMulti.isChecked() == False:#por orden y evitar seleccionar las dos opciones al tiempo
            
            self.checkWelch.setEnabled(True)
            self.tipo_ventana.setEnabled(True)
            self.tamano.setEnabled(True)
            self.solapamiento.setEnabled(True)
            self.frecuencia_w.setEnabled(True)
            self.potencia.setEnabled(True)
        
   
        
        
      
        
        #cuando se cargue la señal se debe volver a habilitarlos
    def asignar_Controlador(self,controlador): #envia la informacion al coordinador 
        self.__coordinador=controlador
    def adelante_senal(self):  # fucnion para delantar la senal dosmil puntos
        self.__x_min=self.__x_min+2000
        self.__x_max=self.__x_max+2000
        self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max)) #le lleva la informacion del movimiento a la senal
            
    def atrasar_senal(self):# fucnion para retroceder la senal dosmil puntos
        #que se salga de la rutina si no puede atrazar
        if self.__x_min<2000:
            return
        self.__x_min=self.__x_min-2000
        self.__x_max=self.__x_max-2000
        self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max))#le lleva la informacion del movimiento a la senal
     
    def wavelet(self): # esta funcion corresponde a la accion del botono del wavelet para llevar la informacion a graficar
        self.__fs = float(int(self.fs.text()))
        
        tiempo, freq, power = self.__coordinador.calcularWavelet(0,self.__fs)
        self.__sc.graficar_espectro(tiempo, freq, power) #le lleva los parametros del tiempo, frecuencia y potencia
        
    def welch(self): #funcion que lleva la informacion para el welch 
        self.__fm = int(self.frecuencia_w.text()) # ingreso de valores necesarios
        self.__ta = int(self.tamano.text())
        self.__so = int(self.solapamiento.text()) #ingreso de valores
        self.__po = int(self.potencia.text())
        f, Pxx = self.__coordinador.calcularWelch(0,self.__fm,self.__ta,self.__so,self.__po) # le envia la informacion necesaria del calculo del welch
        self.__sc2.graficar_analisisw(f,Pxx) # lleva la informacion del welch para ser graficada 
        
    def multitaper(self):#funcion que lleva la informacion para el welch 
        
        self.__fmp = int(self.fs_multi.text()) #ingreso de datos necesarios
        self.__ab = int(self.we.text())
        self.__tam = int(self.tama.text())
        self.__inicial = int(self.ini.text())
        self.__final = int(self.fin.text())
        Pxx, f = self.__coordinador.calcularmulti(0,self.__fmp,self.__ab,self.__tam,self.__inicial,self.__final) #le envia la informacion necesaria para el calculo del multitaper
        self.__sc2.graficar_analisisp(Pxx,f) #lleva la informacion para realizar el grafico
    

#signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, 
#detrend='constant', return_onesided=True, scaling='density', axis=-1)  
    

    # La función QFileDialog muestra el cuadro de diálogo para seleccionar la señal que se quiere cargar 
    # esta funcion se encarga de cargar la informacion de la se�al 
    
    def cargar_senal(self):
        
        archivo_cargado, _ = QFileDialog.getOpenFileName(self,"Abrir senal", "","Todos los archivos(*);;Archivos mat(*.mat)");
        
        if archivo_cargado !="" and archivo_cargado.endswith(".mat"):
            
            print(archivo_cargado)
            data =sio.loadmat(archivo_cargado) # Carga la ruta donde se encuentra guardada la señal en el computador 
            print("Los campos cargados son: " + str(data.keys())); #se evalua las claves del diccionario donde esta guardada la senal
            
            if self.checkojos_abiertos.isChecked(): # si se ha seleccionado el nombre que concuerda con la se�al necesita , se carga
                data = np.squeeze(data['ojos_abiertos']);#para volver la se�al a una sola dimension
                
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data) # le da la informacion al coordinador
                self.__x_min=0
                self.__x_max=4000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max)) # se llama la funcion para graficar la se�al a cargar
                
            
                self.boton_adelante.setEnabled(True) # para asegurar el orden de los botones al ser seleecionado las opciones
                self.boton_atras.setEnabled(True)
                self.checkojos_cerrados.setEnabled(False)
                self.checkanestesia.setEnabled(False)
            
                
            if self.checkojos_cerrados.isChecked():  # si se ha seleccionado el nombre que concuerda con la se�al necesita , se carga
                data = np.squeeze(data['ojos_cerrados']); #para volver la se�al a una sola dimension
                
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data) #le da informacion al coordinador 
                self.__x_min=0
                self.__x_max=4000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max))# se llama la funcion para graficar la se�al a cargar
                #ahora enviandolo al controlador y modelo
            
                self.boton_adelante.setEnabled(True)# para asegurar el orden de los botones al ser seleecionado las opciones
                self.boton_atras.setEnabled(True)
                self.checkojos_abiertos.setEnabled(False)
                self.checkanestesia.setEnabled(False)
                
            if self.checkanestesia.isChecked():  # si se ha seleccionado el nombre que concuerda con la se�al necesita , se carga
                data = np.squeeze(data['anestesia']);#para volver la se�al a una sola dimension
                
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data) #le envia la informacion al controlador 
                self.__x_min=0
                self.__x_max=4000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max))# se llama la funcion para graficar la se�al a cargar
                
                #ahora enviandolo al controlador y modelo
            
                self.boton_adelante.setEnabled(True)# para asegurar el orden de los botones al ser seleecionado las opciones
                self.boton_atras.setEnabled(True)
                self.checkojos_cerrados.setEnabled(False)
                self.checkojos_abiertos.setEnabled(False)
                
            if self.checkojos_abiertos.isChecked()== False:  #con estos condicionales se asegura la posibilidad de solo seleccionar una opcion a la vez
                self.checkojos_cerrados.setEnabled(True)
                self.checkanestesia.setEnabled(True)
                
            if self.checkojos_cerrados.isChecked()== False:
                self.checkojos_abiertos.setEnabled(True)
                self.checkanestesia.setEnabled(True)
                
            if self.checkanestesia.isChecked()== False:
                self.checkojos_cerrados.setEnabled(True)
                self.checkojos_abiertos.setEnabled(True)
               
            
                
             
                    
                
                        
            
            
            
                
                

#app=QApplication(sys.argv)
#mi_ventana = InterfazGrafico()
#sys.exit(app.exec_()) 
             

        
        
        
        