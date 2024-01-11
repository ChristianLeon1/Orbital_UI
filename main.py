
import sys
import pandas as pd 
import numpy as np 
import folium 
from folium.plugins import minimap 
from modules.config_widgets import *
from modules.serial_mod import *
from PySide6.QtCore import QSize, QIODevice, Qt 
from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtGui import QAction, QKeySequence, QResizeEvent, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QToolBar, QComboBox, QLabel, QStatusBar, QFrame, QTabWidget, QWidget, QVBoxLayout, QProgressBar 
# USAR threading para actualizar el puerto serial
import pyqtgraph as pg

class MainWindow(WidgetsIn): 

    def __init__(self) -> None: 
        super(MainWindow, self).__init__()          
        self.app = app 

        self.df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'AltitudGPS':[],'GPS SATS':[],'Sat_pos_x':[],'Sat_pos_y':[],'Autogiro_vel':[],'Estado Software':[]})

        #Inicialización de variables 
        self.baud_rate = None
        self.port = None 

        self.IncluirWidgetsConfig()
        #Configuración serial 
        self.ser = QSerialPort() #Inicialización puerto serial 
        self.ActualizarSerial() # Actualizar los puertos al inicio del programa 

        # Señales 
        #Botones 
        self.boton_actualizar.triggered.connect(self.ActualizarSerial)
        self.boton_conec_ser.triggered.connect(self.ConectarPort) 
        self.boton_descon.triggered.connect(self.DescPort)
        #Combobox  
        self.baud_opts.currentTextChanged.connect(self.GuardarBaudRate)
        self.serial_opts.currentTextChanged.connect(self.GuardarSerialPort)
        # Menubar
        self.salir_app.triggered.connect(self.SalirApp) 
        self.guardar_csv.triggered.connect(self.GuardarCSV)
        #Puerto serial
        self.ser.readyRead.connect(self.LeerDatos) #Leer datos seriales 

    def GuardarBaudRate(self,text):
        self.baud_rate = int(text)
        if self.baud_rate != None and self.serial_opts.currentIndex() != -1: 
            self.boton_conec_ser.setEnabled(True)

    def GuardarSerialPort(self,text): 
        self.port = text 
        if self.baud_rate != None and self.serial_opts.currentIndex() != -1: 
            self.boton_conec_ser.setEnabled(True)

    def ActualizarSerial(self): 
        self.serial_opts.clear()
        self.serial_opts.setEnabled(True)
        if PuertoDisponible() == 0: 
            self.serial_opts.setEnabled(False)
        else: 
            self.serial_opts.addItems(PuertoDisponible())
            self.serial_opts.setCurrentIndex(-1)
        self.port = None
        self.boton_conec_ser.setEnabled(False) 

    def ConectarPort(self):  
        if self.baud_rate != None and self.port != None: 
            self.ser.setPortName(self.port)
            self.ser.setBaudRate(self.baud_rate)
            if self.ser.open(QIODevice.ReadWrite): 
                self.statusBar().showMessage(f'Conectado al puerto {self.port}', 10000)
                self.boton_conec_ser.setEnabled(False)
                self.boton_descon.setEnabled(True)
            else: 
                self.statusBar().showMessage(f'No se pudo conectar al puerto{self.port}', 10000)
        else: 
            self.statusBar().showMessage(f'No se pudo conectar al puerto {self.port}', 10000)

    def LeerDatos(self): 
        if not self.ser.canReadLine(): 
            return 
        try: 
            new_row = str(self.ser.readLine(),'utf-8').strip("\n").split(',')
            for i in range(0,len(new_row)): 
                if new_row[i].isdigit(): 
                    new_row[i] = int(new_row[i]) 
                else: 
                    try: 
                        new_row[i] = float(new_row[i])
                    except: 
                        pass 
            #Identificadores
            self.df.loc[len(self.df.index)] = new_row 
            self.hora.setText(f"{self.df.iloc[len(self.df.index) - 1]['Hora']}")
            self.id.setText(f"{self.df.iloc[len(self.df.index) - 1]['ID']}")
            self.pack.setText(f"{self.df.iloc[len(self.df.index) - 1]['Packet Count']}")
            self.launcht.setText(f"{self.df.iloc[len(self.df.index) - 1]['Mission Time']}")

            #Gráficas 
            self.data_volt.setData(self.df['Packet Count'], self.df['Voltaje'])
            self.data_temp.setData(self.df['Packet Count'], self.df['Temperatura'])
            self.altura.setText(f"{self.df.iloc[len(self.df.index) - 1]['Altitud']}")
            if self.df.iloc[len(self.df.index) - 1]['Altitud'] <= 450:
                self.altura_b.setValue(self.df.iloc[len(self.df.index) - 1]['Altitud'])
            else: 
                self.altura_b.setValue(450)

        except:
            pass

    def DescPort(self): 
        self.boton_conec_ser.setEnabled(True)
        self.boton_descon.setEnabled(False)
        if self.ser.isOpen: 
            self.ser.close()
            self.statusBar().showMessage(f'Se desconecto correctamente el puerto {self.port}', 10000)

    def GuardarCSV(self): 
        if len(self.df.index) > 1: 
            self.df.to_csv(f"Vuelo_{self.df.iloc[len(self.df.index)-1]['ID']}.csv", header =True)
            self.statusBar().showMessage(f"Se guardo correctamente el archivo Vuelo_{self.df.iloc[len(self.df.index)-1]['ID']}.csv", 10000)
        else: 
            self.statusBar().showMessage(f"No se pudo guardar el archivo Vuelo_{self.df.iloc[len(self.df.index)-1]['ID']}.csv", 10000)
           
    def SalirApp(self): #Método para salir de la app, proximamente cerrar el puerto serial antes de salir. 
        self.DescPort()
        self.app.quit()

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec()) 

