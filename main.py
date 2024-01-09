#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

import sys
import pandas as pd 
import numpy as np 
from serial_mod.serial_mod import PuertoDisponible, ColorTab
from PySide6.QtCore import QSize, QIODevice 
from PySide6.QtSerialPort import QSerialPortInfo, QSerialPort
from PySide6.QtGui import QAction, QKeySequence, QResizeEvent, Qt
from PySide6.QtWidgets import QLayout, QMainWindow, QApplication, QToolBar, QComboBox, QLabel, QStatusBar, QFrame, QTabWidget, QWidget
# USAR threading para actualizar el puerto serial 

class MainWindow(QMainWindow): 

    def __init__(self) -> None: 
        super(MainWindow, self).__init__()          #Inicialización de Main Window 
        self.app = app 
        self.df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'AltitudGPS':[],'GPS SATS':[],'Sat_pos_x':[],'Sat_pos_y':[],'Autogiro_vel':[],'Estado Software':[]})

        #Inicialización de variables 
        self.baud_rate = None
        self.port = None 
        
        #Ajustes app 
        # self.setWindowIcon()   #Falta agregar el ícono 
        self.setWindowTitle("Estación Terrena ORBITAL")
        self.setObjectName("Estación Terrena ORBITAL")
        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424")

        # Cuadro con identificadores de la misión. 
        self.frame_data = QFrame(self)
        self.hora_frame = QFrame(self.frame_data) 
        self.id_frame = QFrame(self.frame_data)
        self.launcht_frame = QFrame(self.frame_data)
        self.pack_frame = QFrame(self.frame_data)
        self.hora_label = QLabel(self.hora_frame)
        self.hora_label.setText("HORA")
        self.hora_label.setAlignment(Qt.AlignCenter) 
        self.hora_label.setGeometry(3,3,198,27)
        self.id_label = QLabel(self.id_frame)
        self.id_label.setText("ID")
        self.id_label.setAlignment(Qt.AlignCenter)
        self.id_label.setGeometry(3,3,198,27)
        self.launcht_label = QLabel(self.launcht_frame)
        self.launcht_label.setText("LAUNCH TIME")
        self.launcht_label.setAlignment(Qt.AlignCenter)
        self.launcht_label.setGeometry(3,3,198,27)
        self.pack_label = QLabel(self.pack_frame) 
        self.pack_label.setText("PACK COUNT")
        self.pack_label.setAlignment(Qt.AlignCenter)
        self.pack_label.setGeometry(3,3,198,27)
        self.hora = QLabel(self.frame_data)
        self.id = QLabel(self.frame_data)
        self.launcht = QLabel(self.frame_data)
        self.pack = QLabel(self.frame_data)

        # Cuadro con las señales recibidas de los sensores. 
        self.frame_sensores = QFrame(self)
        self.tab_cont = QTabWidget(self) 
        self.tab_graphs = QWidget()
        self.tab_GPS = QWidget() 
        self.tab_cont.addTab(self.tab_graphs, "Sensores")
        self.tab_cont.addTab(self.tab_GPS,"GPS")
        self.tab_cont.setStyleSheet(ColorTab())

        self.frame_data.setStyleSheet("background: #151515;"
                                    "border: 1px;"
                                    "border-radius: 5px;") 
        self.hora_frame.setStyleSheet("background: #00BDFF;") 
        self.id_frame.setStyleSheet("background: #00BDFF;")
        self.launcht_frame.setStyleSheet("background: #00BDFF;")
        self.pack_frame.setStyleSheet("background: #00BDFF;")
        self.hora_label.setStyleSheet("background: #2A2A2A;"
                                      "color: white;"
                                      "font-size: 16px;"
                                      "font-weight: bold;")
        self.launcht_label.setStyleSheet("background: #2A2A2A;"
                                      "color: white;"
                                      "font-size: 16px;"
                                      "font-weight: bold;")
        self.pack_label.setStyleSheet("background: #2A2A2A;"
                                      "color: white;"
                                      "font-size: 16px;"
                                      "font-weight: bold;")
        self.id_label.setStyleSheet("background: #2A2A2A;"
                                      "color: white;"
                                      "font-size: 16px;"
                                      "font-weight: bold;") 
        self.hora.setStyleSheet("background-color: #2A2A2A;"
                                "font-size: 20px;"
                                "font-weight: bold;")
        self.id.setStyleSheet("background-color: #2A2A2A;"
                                "font-size: 20px;"
                                "font-weight: bold;")
        self.launcht.setStyleSheet("background-color: #2A2A2A;"
                                "font-size: 20px;"
                                "font-weight: bold;")
        self.pack.setStyleSheet("background-color: #2A2A2A;"
                                "font-size: 20px;"
                                "font-weight: bold;")

        self.frame_sensores.setStyleSheet("background-color: #151515;"
                                    "border: 1px 022466;"
                                    "border-radius: 5px;")

        self.setFixedSize(int(1920*0.9), int(1080*0.9))


        #Tamaño de los Widgets
        self.CambioTamano(self.geometry().width(),self.geometry().height())

        #Menubar configuración
        self.menubar = self.menuBar()

        archivo_menu = self.menubar.addMenu("Archivo") 
        guardar_csv = archivo_menu.addAction("Guardar CSV")
        guardar_csv.setShortcut(QKeySequence("Ctrl+s"))
        salir_app = archivo_menu.addAction("Salir")
        salir_app.setShortcut(QKeySequence("Ctrl+q"))
        salir_app.triggered.connect(self.SalirApp) 
        guardar_csv.triggered.connect(self.GuardarCSV)
        
        #Configuración serial 
        
        self.ser = QSerialPort() #Inicialización puerto serial 
        self.ser.readyRead.connect(self.LeerDatos) #Leer datos seriales 

            # Botones 
        self.boton_actualizar = QAction("Actualizar Puertos")
        self.boton_actualizar.triggered.connect(self.ActualizarSerial)

        self.boton_conec_ser = QAction("Conectar")
        self.boton_conec_ser.triggered.connect(self.ConectarPort) 
        self.boton_conec_ser.setEnabled(False)
        
        self.boton_descon = QAction("Desconectar")
        self.boton_descon.triggered.connect(self.DescPort)
        self.boton_descon.setEnabled(False)
        
        #Combo box configuración serial. 
        self.baud_opts = QComboBox()
        self.baud_opts.addItems(['9600', '19200', '31250', '38400', '57600', '74880', '115200', '230400', '250000', '460800', '500000', '921600', '1000000', '2000000'])
        self.baud_opts.setCurrentIndex(-1)
        label_baud = QLabel("Baudrate: ")
        self.baud_opts.currentTextChanged.connect(self.GuardarBaudRate)

        self.serial_opts = QComboBox() 
        label_serial = QLabel("Puertos Disponibles: ")
        self.ActualizarSerial()
        self.serial_opts.currentTextChanged.connect(self.GuardarSerialPort)
        
        #Toolbar 
        self.toolbar = QToolBar("Herramientas") 
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar) 
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(label_baud)
        self.toolbar.addWidget(self.baud_opts)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_serial) 
        self.toolbar.addWidget(self.serial_opts)
        self.toolbar.addAction(self.boton_actualizar)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_conec_ser) 
        self.toolbar.addAction(self.boton_descon)

        # Status Bar 
        self.setStatusBar(QStatusBar(self))

    def CambioTamano(self, width, height): 
        
        # Tamaño y posición de identificadores: 
        self.frame_data.setGeometry(int(width*0.018), int(height*0.08), width - int(width*0.036), int(height*0.185))
        width_f, height_f = self.frame_data.geometry().width(), self.frame_data.geometry().height() 
        self.hora_frame.setGeometry(int(width_f*0.04), int(height_f*0.2), 200, 30) 
        self.launcht_frame.setGeometry(200 + int(width_f*0.07), int(height_f*0.2), 200, 30) 
        self.pack_frame.setGeometry(width_f - 400 - int(width_f*0.07), int(height_f*0.2), 200, 30) 
        self.id_frame.setGeometry(width_f- 200 - int(width_f*0.05), int(height_f*0.2), 200, 30) 
        self.hora.setGeometry(int(width_f*0.04), int(height_f*0.24) + 30, 200, 50)
        self.launcht.setGeometry(200 + int(width_f*0.07), int(height_f*0.24) + 30, 200, 50)
        self.pack.setGeometry(width_f - 400 - int(width_f*0.07), int(height_f*0.24) + 30, 200, 50)
        self.id.setGeometry(width_f- 200 - int(width_f*0.05), int(height_f*0.24) + 30, 200, 50)


        # Tamaño de los datos de los sensores:  
        self.frame_sensores.setGeometry(int(width - width*0.264), int(height*0.3), width - int(width*0.754), int(height*0.65))
        self.tab_cont.setGeometry(int(width*0.018), int(height*0.3), width -int(width*0.3), int(height*0.65))
    

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
            self.df.loc[len(self.df.index)] = new_row 
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

    def resizeEvent(self, event: QResizeEvent) -> None:
        new_width = self.geometry().width()
        new_height = self.geometry().height()
        self.CambioTamano(new_width, new_height)

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_()) 

