#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 AUTOR: Christian Yael Ramírez León

# Interfaz de usuario para la estación terrena de cansat

import sys
import pandas as pd 
import folium 
from modules.config_widgets import *
from modules.serial_mod import *
from PySide6.QtCore import QIODevice, QTimer
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QApplication
import time
# USAR threading para actualizar el puerto serial

class MainWindow(WidgetsIn): 

    def __init__(self) -> None: 

        super(MainWindow, self).__init__()          
        self.app = app 
        self.tiempo_transcur = [0]

        self.df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'AltitudGPS':[],'GPS SATS':[],'Pitch':[],'Roll':[],'Autogiro_vel':[],'Estado Software':[]})

        #Inicialización de variables 
        self.baud_rate = None
        self.port = None 
        self.sensores_timer = QTimer(self)
        self.gps_timer = QTimer(self)
        self.graficas_timer = QTimer(self)
        self.flag = False
        self.posicion = [0,0]
        self.graf_x = 15

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

        #Actualización de datos de los sensores
        self.sensores_timer.timeout.connect(self.ActualizarSensores)
        self.gps_timer.timeout.connect(self.ActualizarGPS)        
        self.graficas_timer.timeout.connect(self.ActualizarGraficas)

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

    def ActualizarGPS(self): 
        if self.flag: 
            
            if not (self.posicion[0] == self.df.iloc[len(self.df.index) - 1]['Latitud'] and self.posicion[1] == self.df.iloc[len(self.df.index) - 1]['Longitud']):
                self.maps = folium.Map(location= [self.df.iloc[len(self.df.index) - 1]['Latitud'], self.df.iloc[len(self.df.index) - 1]['Longitud']], zoom_start=17)
                folium.Marker(location=[self.df.iloc[len(self.df.index) - 1]['Latitud'], self.df.iloc[len(self.df.index) - 1]['Longitud']]).add_to(self.maps)
                self.gps_w.setHtml(self.maps.get_root().render())
                self.posicion = [self.df.iloc[len(self.df.index) - 1]['Latitud'], self.df.iloc[len(self.df.index) - 1]['Longitud']]

    def ActualizarSensores(self): 
        if self.flag: 
            #Identificadores
            self.hora.setText(f"{self.df.iloc[len(self.df.index) - 1]['Hora']}")
            self.id.setText(f"{self.df.iloc[len(self.df.index) - 1]['ID']}")
            self.pack.setText(f"{self.df.iloc[len(self.df.index) - 1]['Packet Count']}")
            self.launcht.setText(f"{self.df.iloc[len(self.df.index) - 1]['Mission Time']}")

            #Mensajes de sensores 
            self.presion.setText(f"{self.df.iloc[len(self.df.index) - 1]['Presión']}")
            self.pitch.setText(f"{self.df.iloc[len(self.df.index) - 1]['Pitch']}")
            self.roll.setText(f"{self.df.iloc[len(self.df.index) - 1]['Roll']}")
            self.rpm.setText(f"{self.df.iloc[len(self.df.index) - 1]['Autogiro_vel']}")
            self.estado.setText(f"{self.df.iloc[len(self.df.index) - 1]['Estado Software']}")
            #Falta poner la velocidad. 
            if len(self.df.index) > 1: 
                self.velocidad.setText(f"{round((self.df.iloc[len(self.df.index) - 2]['Altitud'] - self.df.iloc[len(self.df.index) - 1]['Altitud']) / (self.tiempo_transcur[len(self.tiempo_transcur) - 1] - self.tiempo_transcur[len(self.tiempo_transcur) - 2]), 2)}")
            else: 
                self.velocidad.setText(f"0.0")

    def ActualizarGraficas(self):
        if not self.tiempo_transcur[len((self.df.index)) - 1] < self.graf_x: 
            self.graf_x += 15
            self.volt.setXRange(self.graf_x - 15, self.graf_x)
            self.temp.setXRange(self.graf_x - 15, self.graf_x)
        self.volt.data.setData(self.tiempo_transcur, self.df['Voltaje'])
        self.temp.data.setData(self.tiempo_transcur, self.df['Temperatura'])

        self.altura.setText(f"{self.df.iloc[len(self.df.index) - 1]['Altitud']} m")
        if self.df.iloc[len(self.df.index) - 1]['Altitud'] <= 500:
            self.altura_b.setValue(self.df.iloc[len(self.df.index) - 1]['Altitud'])
        else: 
            self.altura_b.setValue(500)
            
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
            self.df.loc[len(self.df.index)] = new_row  

            if not self.flag: 
                self.flag = True
                self.tiempo_inic = time.time()
                self.sensores_timer.start(500)
                self.gps_timer.start(3007)
                self.graficas_timer.start(73)
                self.ActualizarGPS()
                self.ActualizarSensores() 
                self.ActualizarGraficas()
            else: 
                self.tiempo_transcur.append(time.time() - self.tiempo_inic)
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

