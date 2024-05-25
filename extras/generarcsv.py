#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

# Genera un csv de prueba para guardarlo y simular la recepción de datos de la telemetría de la misión. 

import pandas as pd 
import random 
import numpy as np
df = pd.DataFrame({'ID':[],'Tiempo de misión':[],'Contador de paquetes':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'Pitch':[],'Roll':[],'Aceleración':[],'Estado Software':[]})

a = []

x = np.linspace(0,100,6000) 
subir = (9.81*(x - 20)**2)/2 
bajar = ((9.81)*(10)**2)/2 - ((9.81)*(x- 30)**2)/2
vel_const = ((9.81)*(10)**2)/2 - ((9.81)*(37 - 30)**2)/2 - (x-37)*10 

for i in range(0,100): 
  for j in range(0,60): 
    for h in range(0,2): 

        #ID
        if h == 0: 
            a.append("1")
        else:
            a.append("2")

        #Time
        if j == 0: 
            a.append(0)
        else:
            a.append(round(i + 1/j, 3))  
        #Packet Count
        a.append(i*60 + j + 1)
        
        #Altitud
        if i*60 + j < 20*60: 
            a.append(0)
        elif 20*60 <= i*60 + j and i*60 + j < 30*60:
            a.append(round(subir[i*60 + j],1))
        elif 30*60 <= i*60 + j and i*60 + j < 37*60: 
            a.append(round(bajar[i*60 + j],1))
        elif 37*60 <= i*60 + j and i*60 + j <62*60: 
            a.append(round(vel_const[i*60 + j],1))
        else: 
            a.append(0)
        
        #Presion
        a.append(round(random.uniform(77410 - 10, 77410 +10),1))
        #Temperatura
        a.append(round(random.randint(20,24)))
        #Voltaje
        a.append(round(random.uniform(5,9),2))
        #Hora
        if i < 10: 
            a.append(f'11:29:0{i}')
        elif 10 <= i and i <60: 
            a.append(f'11:29:{i}')
        elif 60 <= i and i < 70: 
            a.append(f'11:30:0{i-60}')
        else: 
            a.append(f'11:30:{i-60}')  
        #Latitud
        a.append(round(random.uniform(19.502454291471974,19.50264291471974),5))
        #Longitud
        a.append(-round(random.uniform(99.13312701719184, 99.13332701719184),5))

        #Sat_pos_x
        a.append(round(random.randint(0,10)))
        #Sat_pos_y
        a.append(round(random.randint(0,10)))
        #Aceleración de caida 
        a.append(round(0))
        # Estado del Software
        a.append("BOOT\\r")
        df.loc[len(df.index)] = a 
        a = [] 

print(df)

df.to_csv("Datos_mis_simul.csv", header = False, index=False)
