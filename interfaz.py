
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
import csv # Librería que ayuda 
import scipy.io as sio  # Librería científica que soporta la carga de multiples tipos de archivos
import numpy as np # librería que permite trabajar con arrays
import matplotlib.pyplot as plt;
import scipy.signal as signal;
import matplotlib.pyplot as plt;
from Modelo import Biosenal # Del archivo Modelo se importa la  



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
        
    def __init2__(self,parent= None,width=3, height=3, dpi=90):
        
        self.fig2= Figure(figsize=(width, height), dpi=dpi)
        self.axes2= self.fig.add_subplot(211)
        
        FigureCanvas.__init2__(self,self.fig2)
  
#segundo espacio para graficar el espectro      
    def graficar_espectro(self,datos):
        
        self.axes2.clear()
        self.axes2.subplot(datos)
        self.axes2.set_xlabel("Tiempo")
        self.axes2.set_ylabel("Amplitud")
        self.axes2.figure.canvas.draw()
        
        pass
        
    
   
    # Se crea un metodo para graficar lo que se desee
    def graficar_senal(self,datos):
        # primero se necesita limpiar la grafica anterior
        self.axes.clear()
        #Se ingresan los datos a graficar y se grafican
    
 #Se grafican las señales en un mismo plano de forma que no queden superpuestas, cuando se utiliza plot las señales quedan en la misma gráfica
        if datos.ndim==1: # Si la señal es de una dimensión, se grafica la señal
            self.axes.plot(datos)
            print("datos")
            print(datos)
            
#Si la señal es de múltiples dimensiones entonces se conoce cuantos canales tiene la señal mediante mediante la función shape 
#y se grafican todos los canales
          
        else: 
            DC=14
            for canal in range(datos.shape[0]):
                self.axes.plot(datos[canal,:] + DC*canal) # Grafica todos los canales
       
        
        self.axes.set_xlabel("Tiempo") # Al eje x se le asigna el nombre Tiempo
        self.axes.set_ylabel("Amplitud") # Al eje y se le asigna el nombre amplitud
        #self.axes.set
        
        self.axes.figure.canvas.draw() # Se da la indidicación de que se dibuje la figura
        
       
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
        self.campo_filtrada.setLayout(layout2)
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_graficacion, width=5, height=4, dpi=100)
        self.__sc2 = MyGraphCanvas(self.campo_filtrada, width=5, height=4, dpi=100)
        #se añade el campo de graficos
        layout.addWidget(self.__sc)
        layout2.addWidget(self.__sc2)
        
        #se organizan las señales 
        self.boton_cargarsenal.clicked.connect(self.cargar_senal)  # El usuario puede dar click sobre el botón para cargar la señal
        #El botón desplazamiento en el tiempo tiene la opción de adelantar o atrasar la señal cargada
        self.boton_adelante.clicked.connect(self.adelante_senal) 
        self.boton_atras.clicked.connect(self.atrasar_senal)
        
        # El usuario puede escribir el número del canal que desee visualizar y da clic en seleccionar canal
        self.seleccion_canal.clicked.connect(self.graficar_canal) 
        self.campo.setValidator(QIntValidator(0,10))  # Se asigna un QInt Validator para que se tomen canales entre 0 y 10
         
 #Los botones adelantar y atrasar señal asociados al desplazamiento de la señal no se habilitan si la señal no esta cargada
        self.boton_adelante.setEnabled(False)
        self.boton_atras.setEnabled(False)
        self.seleccion_canal.setEnabled(False) 
        # El botón seleccionar canal no esta disponible si el usuario no ha cargado la señal
        

    
            
   
        
            
        
       
    def graficar_canal(self): # Función que selecciona el canal
        canal = int (self.campo.text())  # se ingresa el canal en el campo canal. Ese campo es una cadena entonces debe convertirse en entero
        
        self.__sc.graficar_senal(self.__coordinador.devolver_canal(canal,self.__x_min,self.__x_max))
            
        self.boton_cargarsenal.setEnabled(True)
        self.boton_adelante.setEnabled(False)  # Se deshabilitan los botones de desplzamiento de la señal a la hora de graficar el canal
        self.boton_atras.setEnabled(False)
      
        
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
        
        
#se necesita organizar que cargue cualquier tipo de senal .mat, para ello se necesita programaar y ser cuidadoso con los diccionarios con la longitud 
#y las dimensiones 
    
    def cargar_senal(self):
    # La función QFileDialog muestra el cuadro de diálogo para seleccionar la señal que se quiere cargar 
        archivo_cargado, _ = QFileDialog.getOpenFileName(self,"Abrir senal", "","Todos los archivos(*);;Archivos mat(*.mat)");
        
        if archivo_cargado !="" and archivo_cargado.endswith(".mat"): # Para poder cargar la señal este debe ser de formato .mat
            print(archivo_cargado)
            data=sio.loadmat(archivo_cargado) # Carga la ruta donde se encuentra guardada la señal en el computador 
            print("Los campos cargados son: " + str(data.keys()));
            data = np.squeeze(data['data']); # Vector donde se almacena la señal
            
            #data = data["data"] # El archivo .mat contiene un campo data en el cual se encuentra la señal
 # El data que contiene la señal es tridimimensional, contiene sensores, puntos y ensayos. Si la señal es bidimensional se arroja un error
            sensores,puntos,ensayos=data.shape # Sensores: filas, Puntos: columnas, ensayos: matrices 
            senal_continua=np.reshape(data,(sensores,puntos*ensayos),order="F") # Se genera una señal continua
            
 #el coordinador, el cual puede encontrarse ene l controlador se encarga de recibir y guardar la señal en su propio .py, 
 #por eso no se requiere una variable que lo guarde en el .py interfaz
            self.__coordinador.recibirDatosSenal(senal_continua)
            self.__x_min = 0 
# xmin y xmax son variables que permiten al usuario mover la señal entre 0 y 2000 puntos, están asociadas a,los botones de desplazamiento
            self.__x_max = 2000
            #graficar utilizando el controlador
            self.__sc.graficar_senal(self.__coordinador.devolverDatosSenal(self.__x_min,self.__x_max))  # Se grafica la señal y se tiene en cuenta los limites establecidos
            self.boton_adelante.setEnabled(True)
            self.boton_atras.setEnabled(True)
            self.seleccion_canal.setEnabled(True)
    
#        
#app=QApplication(sys.argv)
#mi_ventana = InterfazGrafico()
#sys.exit(app.exec_()) 
#               
        
        
        
        
        
        
        