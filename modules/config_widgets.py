#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction, QKeySequence, QResizeEvent, Qt
from PySide6.QtWidgets import QMainWindow, QToolBar, QComboBox, QLabel, QStatusBar, QFrame, QTabWidget, QVBoxLayout, QProgressBar 

from PySide6.QtWebEngineWidgets import QWebEngineView
from modules.tab_style import ColorTab
import pyqtgraph as pg
import folium 

class WidgetsIn(QMainWindow): 
    def IncluirWidgetsConfig(self): 
        #Ajustes app 
        # self.setWindowIcon()   #Falta agregar el ícono 
        self.setWindowTitle("Estación Terrena ORBITAL")
        self.setObjectName("Estación Terrena ORBITAL")
        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424")
        self.setFixedSize(int(1920*0.9), int(1080*0.9))

        #Menubar 
        self.menubar = self.menuBar()
        self.archivo_menu = self.menubar.addMenu("Archivo") 
        self.guardar_csv = self.archivo_menu.addAction("Guardar CSV")
        self.guardar_csv.setShortcut(QKeySequence("Ctrl+s"))
        self.salir_app = self.archivo_menu.addAction("Salir")
        self.salir_app.setShortcut(QKeySequence("Ctrl+q"))

        #Toolbar 
        self.toolbar = QToolBar("Herramientas") 
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar) 
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        #Combo box configuración serial. 
        label_baud = QLabel("Baudrate: ")
        self.baud_opts = QComboBox()
        self.baud_opts.addItems(['9600', '19200', '31250', '38400', '57600', '74880', '115200', '230400', '250000', '460800', '500000', '921600', '1000000', '2000000'])
        self.baud_opts.setCurrentIndex(-1)
        self.serial_opts = QComboBox() 
        label_serial = QLabel("Puertos Disponibles: ")

        # Botones 
        self.boton_actualizar = QAction("Actualizar Puertos")
        self.boton_conec_ser = QAction("Conectar")
        self.boton_descon = QAction("Desconectar")
        self.boton_conec_ser.setEnabled(False)
        self.boton_descon.setEnabled(False)
        
        #Widgets en el toolbar 
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
        self.hora.setAlignment(Qt.AlignCenter)
        self.id = QLabel(self.frame_data)
        self.id.setAlignment(Qt.AlignCenter)
        self.launcht = QLabel(self.frame_data)
        self.launcht.setAlignment(Qt.AlignCenter)
        self.pack = QLabel(self.frame_data)
        self.pack.setAlignment(Qt.AlignCenter)
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

        #Sensores 
        self.frame_sensores = QFrame(self)
        self.frame_sensores.setStyleSheet("background-color: #151515;"
                                    "border: 1px 022466;"
                                    "border-radius: 5px;")
        self.presion_label = QLabel(self.frame_sensores)
        self.giros_x_label = QLabel(self.frame_sensores)
        self.giros_y_label = QLabel(self.frame_sensores)
        self.rpm_label = QLabel(self.frame_sensores)
        self.velocidad_label = QLabel(self.frame_sensores)
        self.estado_label = QLabel(self.frame_sensores)
        self.presion_label.setText("PRESIÓN:")
        self.giros_x_label.setText("GIROSCOPIO X:")
        self.giros_y_label.setText("GIROSCOPIO Y:")
        self.rpm_label.setText("RPM:")
        self.velocidad_label.setText("VELOCIDAD:")
        self.estado_label.setText("ESTADO:")
        self.presion_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.giros_x_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.giros_y_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.rpm_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.velocidad_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.estado_label.setStyleSheet("font-size: 20px;"
                                "font-weight: bold;")
        self.presion = QLabel(self.frame_sensores)
        self.giros_x = QLabel(self.frame_sensores)
        self.giros_y = QLabel(self.frame_sensores)
        self.rpm = QLabel(self.frame_sensores)
        self.velocidad = QLabel(self.frame_sensores)
        self.estado = QLabel(self.frame_sensores)
        self.presion.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.giros_x.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.giros_y.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.rpm.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.velocidad.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.estado.setStyleSheet("background: #2A2A2A;"
                                     "color: white;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")
        self.presion.setAlignment(Qt.AlignCenter)
        self.giros_x.setAlignment(Qt.AlignCenter)
        self.giros_y.setAlignment(Qt.AlignCenter)
        self.rpm.setAlignment(Qt.AlignCenter)
        self.velocidad.setAlignment(Qt.AlignCenter)
        self.estado.setAlignment(Qt.AlignCenter)


        #Tabs 
        self.tab_cont = QTabWidget(self) 
        self.tab_graphs = QFrame()
        self.tab_GPS = QFrame() 
        self.tab_cont.setStyleSheet(ColorTab())
        self.tab_cont.addTab(self.tab_graphs, "Sensores")
        self.tab_cont.addTab(self.tab_GPS,"GPS")

        #Tab Graficas
        self.tab_graphs.setStyleSheet("border-radius: 5px;")
        self.altura_frame = QFrame(self.tab_graphs)
        self.temp_frame = QFrame(self.tab_graphs) 
        self.volt_frame = QFrame(self.tab_graphs) 
        self.altura_frame.setStyleSheet("background: #151515")
        self.temp_frame.setStyleSheet("background: #151515")
        self.volt_frame.setStyleSheet("background: #151515")
        self.volt_container = QVBoxLayout(self.volt_frame)
        self.volt = pg.PlotWidget()
        self.volt.showGrid(x=True, y=True)
        self.volt.setLabel('left', 'Voltaje', units='v')
        self.volt.setLabel('bottom', 'Tiempo', units='s')
        self.volt_container.addWidget(self.volt)
        self.volt.setYRange(0,10)
        self.data_volt = self.volt.plot([],[])
        self.temp_container = QVBoxLayout(self.temp_frame)
        self.temp = pg.PlotWidget()
        self.temp_container.addWidget(self.temp)
        self.temp.setYRange(0,30)
        self.data_temp = self.temp.plot([],[])
        self.altura_b = QProgressBar(self.altura_frame)
        self.altura_b.setOrientation(Qt.Vertical)
        self.altura_b.setStyleSheet("""QProgressBar{
                                  border: 2px solid white;
                                  border-radius: 5px;
                                  text-align: center; 
                                  }
                                  QProgressBar::chunk {
                                  background-color: red;
                                  }""")    
        self.altura_b.setTextVisible(False)
        self.altura_b.setRange(0,500) 
        self.altura_frame_name = QFrame(self.altura_frame)
        self.altura_label = QLabel(self.altura_frame_name) 
        self.altura = QLabel(self.altura_frame) 
        self.altura_label.setText("ALTITUD")
        self.altura_label.setAlignment(Qt.AlignCenter)
        self.altura.setAlignment(Qt.AlignCenter)
        self.altura_frame_name.setStyleSheet("background-color: #00BDFF")
        self.altura_label.setStyleSheet("background: #2A2A2A;"
                                        "color: white;"
                                        "font-size: 16px;"
                                        "font-weight: bold;")
        self.altura.setStyleSheet("background: #2A2A2A;"
                                  "color: white;"
                                  "font-size: 16px;"
                                  "font-weight: bold;")

        #Tab GPS
        self.tab_GPS.setStyleSheet("border-radius: 5px;")
        self.gps_frame = QFrame(self.tab_GPS)
        self.gps_w = QWebEngineView(self.gps_frame)
        self.maps = folium.Map(location = [19.4284, -99.1276], zoom_start=4)
        self.gps_w.setHtml(self.maps.get_root().render())

        self.gps_frame.setStyleSheet("background: #151515")



    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.geometry().width()
        height = self.geometry().height()

        #Tab
        self.tab_cont.setGeometry(int(width*0.018), int(height*0.3), width -int(width*0.3), int(height*0.65))
        width_f, height_f = self.tab_cont.geometry().width(), self.tab_cont.geometry().height()

        #GPS 
        # width_f,height_f = self.tab_GPS.geometry().width(), self.tab_GPS.geometry().height()
        self.gps_frame.setGeometry(int(0.01*width_f), int(0.01*height_f), int(0.6*width_f), int(0.9*height_f) - 31)
        self.gps_w.setGeometry(int(0.05*self.gps_frame.geometry().width()), int(0.05*self.gps_frame.geometry().height()), int(0.9*self.gps_frame.geometry().width()), int(0.9*self.gps_frame.geometry().height()))

        # Gráficas 
        self.altura_frame.setGeometry(int(width_f*0.01), int(height_f*0.02), int(width*0.09), height_f - int(height_f*0.04) - 31)
        self.volt_frame.setGeometry(int(width_f*0.15), int(height_f*0.1), int(width_f*0.41), height_f - int(height_f*0.2) - 31) 
        self.temp_frame.setGeometry(int(width_f*0.575), int(height_f*0.1), int(width_f*0.41), height_f - int(height_f*0.2) - 31) 
        width_f, height_f = self.altura_frame.geometry().width(), self.altura_frame.geometry().height()
        self.altura_b.setGeometry(int(width_f*0.45),int(height_f*0.05),int(width_f*0.1), int(height_f*0.75))
        self.altura_frame_name.setGeometry(int(width_f*0.1), int(height_f*0.82), int(width_f*0.8), 30)
        self.altura_label.setGeometry(3,3,self.altura_frame_name.geometry().width() - 3, 28)
        self.altura.setGeometry(int(width_f*0.1), int(height_f*0.9), int(width_f*0.8), 30)
    
        # Identificadores: 
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

        # Datos de los sensores:  
        self.frame_sensores.setGeometry(int(width - width*0.264), int(height*0.3), width - int(width*0.754), int(height*0.65)) 
        width_f, height_f = self.frame_sensores.geometry().width(), self.frame_sensores.geometry().height() 
        self.presion_label.setGeometry(int(width_f*0.1), int(height_f/7) - 15, int(width_f*0.4), 30)
        self.giros_x_label.setGeometry(int(width_f*0.1), 2*int(height_f/7) - 15, int(width_f*0.4), 30)
        self.giros_y_label.setGeometry(int(width_f*0.1), 3*int(height_f/7) - 15, int(width_f*0.4), 30)
        self.rpm_label.setGeometry(int(width_f*0.1),  4*int(height_f/7) - 15, int(width_f*0.4), 30)
        self.velocidad_label.setGeometry(int(width_f*0.1), 5*int(height_f/7) - 15, int(width_f*0.4), 30)
        self.estado_label.setGeometry(int(width_f*0.1), 6*int(height_f/7) - 15, int(width_f*0.4), 30)
        self.presion.setGeometry(int(width_f*0.6), int(height_f/7) - 15, int(width_f*0.3), 30)
        self.giros_x.setGeometry(int(width_f*0.6), 2*int(height_f/7) - 15, int(width_f*0.3), 30)
        self.giros_y.setGeometry(int(width_f*0.6), 3*int(height_f/7) - 15, int(width_f*0.3), 30)
        self.rpm.setGeometry(int(width_f*0.6), 4*int(height_f/7) - 15, int(width_f*0.3), 30)
        self.velocidad.setGeometry(int(width_f*0.6), 5*int(height_f/7) - 15, int(width_f*0.3), 30)
        self.estado.setGeometry(int(width_f*0.6), 6*int(height_f/7) - 15, int(width_f*0.3), 30)
        
        
