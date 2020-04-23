
"""Trabajo numero 2 analisis Espectral Bioseñales
autores: Laura Marcela Berrio, Maria Paulina Salazar Meneses"""




# EN ESTE CÓDIGO SE INCLUYE TODO LO QUE ESTE RELACIONADO CON LA INFORMACIÓN QUE SE RECIBE Y SE LE DA AL USUARIO 
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

 #Se grafican las señales en un mismo plano de forma que no queden superpuestas, 
 #cuando se utiliza plot las señales quedan en la misma gráfica
 
    # Se crea un metodo para graficar lo que se desee
        
    def graficar_senal(self,datos):
        self.axes.clear()
        #Se ingresan los datos a graficar y se grafican
        self.axes.plot(datos)
        print("datos")
        print(datos)
   
        self.axes.set_xlabel("Muestras") # Al eje x se le asigna el nombre muestras
        self.axes.set_ylabel("Amplitud") # Al eje y se le asigna el nombre amplitud
        #self.axes.set
        
        self.axes.figure.canvas.draw() # Se da la indidicación de que se dibuje la figura
        
        
        
        
    def graficar_espectro(self,time, freqs, power):
        self.axes.clear()
        self.axes.contourf(time,
                 freqs[(freqs >= 4) & (freqs <= 40)],
                 power[(freqs >= 4) & (freqs <= 40),:],
                 20, # Especificar 20 divisiones en las escalas de color 
                 extend='both')
        print("datos")
        self.axes.set_ylabel('frequency [Hz]')
        self.axes.set_xlabel('Time [s]')
        self.axes.figure.canvas.draw()#ordenamos que dibuje
        
    def graficar_analisisw(self,f,Pxx):
        #self.axes.clear()
        self.axes.plot(f[(f >= 4) & (f <= 40)],Pxx[(f >= 4) & (f <= 40)])
        self.axes.set_ylabel('frequency [Hz]')
        self.axes.set_xlabel('Time [s]')
        self.axes.figure.canvas.draw()#ordenamos que dibuje
        
    def graficar_analisisp(self,Pxx,f):
        
        self.axes.plot(f[(f >= 4) & (f <= 40)],Pxx[(f >= 4) & (f <= 40)])
        self.axes.set_ylabel('frequency [Hz]')
        self.axes.set_xlabel('Time [s]')
        self.axes.figure.canvas.draw()

#signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, 
#detrend='constant', return_onesided=True, scaling='density', axis=-1)
#f, Pxx = signal.welch(ecg,fs,'hamming', 512*0.5, 256*0.5, 512*0.5, scaling='density');

   
    
        
                 
       
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
        self.__sc = MyGraphCanvas(self.campo_graficacion, width=5, height=4, dpi=100)
        self.__sc2 = MyGraphCanvas(self.campo_w, width=5, height=4, dpi=100)
        
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
        
        #los botones, checkbox y combobox para el analisis espectral
        self.checkWelch.stateChanged.connect(self.cambio)
        self.checkMulti.stateChanged.connect(self.cambio)
       
        self.tipo_ventana.addItem("hamming")
        
    
        
    
    def cambio(self):
        
        if self.checkWelch.isChecked() == True:
            
            self.checkMulti.setEnabled(False) #por orden y evitar seleccionar las dos opciones al tiempo
            self.fs_multi.setEnabled(False)
            self.w.setEnabled(False)
            self.T.setEnabled(False)
           
        
        if self.checkMulti.isChecked() == True:
            
            self.checkWelch.setEnabled(False)
            self.tipo_ventana.setEnabled(False)
            self.tamano.setEnabled(False)
            self.solapamiento.setEnabled(False)
            self.frecuencia_w.setEnabled(False)
            
        if self.checkWelch.isChecked() == False:
            
            self.checkMulti.setEnabled(True)
            self.fs_multi.setEnabled(True)
            self.w.setEnabled(True)
            self.T.setEnabled(True)
            
        if self.checkMulti.isChecked() == False:
            
            self.checkWelch.setEnabled(True)
            self.tipo_ventana.setEnabled(True)
            self.tamano.setEnabled(True)
            self.solapamiento.setEnabled(True)
            self.frecuencia_w.setEnabled(True)
        
   
        
            
        
       
    #def graficar_canal(self): # Función que selecciona el canal
        #canal = int (self.campo.text())  # se ingresa el canal en el campo canal. Ese campo es una cadena entonces debe convertirse en entero
        
        #self.__sc.graficar_senal(self.__coordinador.devolver_canal(canal,self.__x_min,self.__x_max))
            
        
      
        
        #cuando se cargue la señal se debe volver a habilitarlos
    def asignar_Controlador(self,controlador):
        self.__coordinador=controlador
    def adelante_senal(self):
        self.__x_min=self.__x_min+2000
        self.__x_max=self.__x_max+2000
        self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max))
            
    def atrasar_senal(self):
        #que se salga de la rutina si no puede atrazar
        if self.__x_min<2000:
            return
        self.__x_min=self.__x_min-2000
        self.__x_max=self.__x_max-2000
        self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max))
     
    def wavelet(self):
        self.__fs = float(int(self.fs.text()))
        
        tiempo, freq, power = self.__coordinador.calcularWavelet(0,self.__fs)
        self.__sc.graficar_espectro(tiempo, freq, power)
        
    def welch(self):
        self.__fm = int(self.frecuencia_w.text())
        self.__ta = int(self.tamano.text())
        self.__so = int(self.solapamiento.text())
        self.__po = int(self.potencia.text())
        f, Pxx = self.__coordinador.calcularWelch(0,self.__fm,self.__ta,self.__so,self.__po)
        self.__sc2.graficar_analisisw(f,Pxx)
        
    def multitaper(self):
        self.__fmp = int(self.fs_multi.text())
        self.__ab = int(self.w.text())
        self.__tam = int(self.T.text())
        Pxx, f = self.__coordinador.calcularmulti(0,self.__fmp,self.__ab,self.__tam)
        self.__sc2.graficar_analisisp(Pxx,f)
    

#signal.welch(x, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, 
#detrend='constant', return_onesided=True, scaling='density', axis=-1)  
    

    # La función QFileDialog muestra el cuadro de diálogo para seleccionar la señal que se quiere cargar 
    
    
    def cargar_senal(self):
        
        archivo_cargado, _ = QFileDialog.getOpenFileName(self,"Abrir senal", "","Todos los archivos(*);;Archivos mat(*.mat)");
        
        if archivo_cargado !="" and archivo_cargado.endswith(".mat"):
            
            print(archivo_cargado)
            data =sio.loadmat(archivo_cargado) # Carga la ruta donde se encuentra guardada la señal en el computador 
            print("Los campos cargados son: " + str(data.keys()));
            
            if self.checkojos_abiertos.isChecked():
                data = np.squeeze(data['ojos_abiertos']);
                sensores=1
                ensayos=1
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data)
                self.__x_min=0
                self.__x_max=8000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max))
                
                #ahora enviandolo al controlador y modelo
            
                self.boton_adelante.setEnabled(True)
                self.boton_atras.setEnabled(True)
                self.checkojos_cerrados.setEnabled(False)
                self.checkanestesia.setEnabled(False)
            
                
            if self.checkojos_cerrados.isChecked():
                data = np.squeeze(data['ojos_cerrados']);
                sensores=1
                ensayos=1
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data)
                self.__x_min=0
                self.__x_max=8000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max))
                
                #ahora enviandolo al controlador y modelo
            
                self.boton_adelante.setEnabled(True)
                self.boton_atras.setEnabled(True)
                self.checkojos_abiertos.setEnabled(False)
                self.checkanestesia.setEnabled(False)
                
            if self.checkanestesia.isChecked():
                data = np.squeeze(data['anestesia']);
                sensores=1
                ensayos=1
                puntos = data.shape[0]
                senal_continua = data
                self.__coordinador.recibirDatosSenal(data)
                self.__x_min=0
                self.__x_max=8000
                self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min, self.__x_max))
                
                #ahora enviandolo al controlador y modelo
            
                self.boton_adelante.setEnabled(True)
                self.boton_atras.setEnabled(True)
                self.checkojos_cerrados.setEnabled(False)
                self.checkojos_abiertos.setEnabled(False)
                
            
                
             
                    
                
                        
            
            
            
                
                

#app=QApplication(sys.argv)
#mi_ventana = InterfazGrafico()
#sys.exit(app.exec_()) 
             

        
        
        
        