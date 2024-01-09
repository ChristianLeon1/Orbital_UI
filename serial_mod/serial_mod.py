#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2023 CREADOR: Christian Yael Ramírez León

import serial 
import time 
import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt 
import subprocess 

# df = pd.DataFrame({
#     'ID',
#     'Mission Time',  
#     'Packet Count',
#     'Altitud', 
#     'Presión', 
#     'Temperatura', 
#     'Voltaje', 
#     'Hora', 
#     'Latitud', 
#     'Longitud',
#     'Altitud',
#     'Sat_pos_x',
#     'Sat_pos_y',
#     'Autogiro_vel'
#     })

# columns_names = df.columns 

# Saber cual puerto está habilitado 

def PuertoDisponible(): 
    port = subprocess.run(['python3', '-m', 'serial.tools.list_ports'], capture_output=True) 
    port = str(port.stdout, 'utf-8')
    if len(port) == 0: 
        return 0 
    port = port.split('\n')
    port.remove('')
    for i in range(0,len(port)): 
        port[i] = port[i].strip()
    return port 
def ColorTab(): 
    return """
QTabWidget::pane {
    border: 1px solid black;
    background: white;
    border-radius: 3px; 
}

QTabWidget::tab-bar:top {
    top: 1px;
}

QTabWidget::tab-bar:bottom {
    bottom: 1px;
}

QTabWidget::tab-bar:left {
    right: 1px;
}

QTabWidget::tab-bar:right {
    left: 1px;
}

QTabBar::tab {
    border: 1px solid black;
    border-radius: 3px;

}

QTabBar::tab:selected {
    background: #022466;
}

QTabBar::tab:!selected {
    background: #242424;
}

QTabBar::tab:!selected:hover {
    background: #303030;
}

QTabBar::tab:top:!selected {
    margin-top: 3px;
}

QTabBar::tab:bottom:!selected {
    margin-bottom: 3px;
}

QTabBar::tab:top, QTabBar::tab:bottom {
    min-width: 8ex;
    margin-right: -1px;
    padding: 5px 10px 5px 10px;
}

QTabBar::tab:top:selected {
    border-bottom-color: none;
}

QTabBar::tab:bottom:selected {
    border-top-color: none;
}

QTabBar::tab:top:last, QTabBar::tab:bottom:last,
QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
    margin-right: 0;
}

QTabBar::tab:left:!selected {
    margin-right: 3px;
}

QTabBar::tab:right:!selected {
    margin-left: 3px;
}

QTabBar::tab:left, QTabBar::tab:right {
    min-height: 8ex;
    margin-bottom: -1px;
    padding: 10px 5px 10px 5px;
}

QTabBar::tab:left:selected {
    border-left-color: none;
}

QTabBar::tab:right:selected {
    border-right-color: none;
}

QTabBar::tab:left:last, QTabBar::tab:right:last,
QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
    margin-bottom: 0;
}
""" 
