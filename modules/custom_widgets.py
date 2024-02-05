#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 Autor: Christian Yael Ramírez León
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QFrame, QLabel 
import pyqtgraph as pg 

class CustomLabel(QLabel):
    def __init__(self, text="", parent=None, fsize=16, background="#2A2A2A", align=Qt.AlignCenter):
        super().__init__(text, parent)

        # Establecer las características iniciales
        self.setStyleSheet(
            f"background: {background};"
            "color: white;"
            f"font-size: {fsize}px;"
            "font-weight: bold;")
        
        self.setAlignment(align)
        self.setGeometry(3,3,198,27)

class CustomFrame(QFrame): 
    def __init__(self, parent=None, background="#000000"):
        super().__init__(parent)
        self.setStyleSheet(f"background: {background};"
                           "border: 1px;"
                           "border-radius: 5px;") 

class CustomGraph(pg.PlotWidget):
    def __init__(self, name="", units="",  pen=pg.mkPen("#0BBB10"), brush=(52,131,54,50), parent=None):
        super().__init__(parent)
        self.showGrid(x=True, y=True) 
        self.setLabel('left', name, units=units)
        self.setLabel('bottom', 'Tiempo', units='s')
        self.setXRange(0,15)
        self.data = self.plot(pen=pen,fillLevel=0, brush=brush)


