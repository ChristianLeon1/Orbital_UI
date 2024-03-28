#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

# Genera un csv de prueba para guardarlo y simular la recepción de datos de la telemetría de la misión. 

import pandas as pd 
import random 
import numpy as np
df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud 1':[],'Longitud 1':[],'GPS SATS':[],'Pitch':[],'Roll':[],'Autogiro_vel':[],'Estado Software':[],'Latitud 2':[],'Longitud 2':[], 'Altitud 2':[]})

a = []

x = np.linspace(0,100,6000) 
subir = (9.81*(x - 20)**2)/2 
bajar = ((9.81)*(10)**2)/2 - ((9.81)*(x- 30)**2)/2
vel_const = ((9.81)*(10)**2)/2 - ((9.81)*(37 - 30)**2)/2 - (x-37)*10 

for i in range(0,100): 
    for j in range(0,60): 

        #ID
        a.append("#ORB")

        #Time
        if i < 10: 
            a.append(f'0:00:0{i}')
        elif 10 <= i and i <60: 
            a.append(f'0:00:{i}')
        elif 60 <= i and i < 70: 
            a.append(f'0:01:0{i-60}')
        else: 
            a.append(f'0:01:{i-60}')

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
            print(i*60 + j, x[i*60 + j], vel_const[i*60 + j])
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
        a.append(round(random.uniform(19.331,19.332),4))
        #Longitud
        a.append(- round(random.uniform(99.193,99.195),4))
        #GPS SATS
        a.append(2)
        #Sat_pos_x
        a.append(round(random.randint(0,10)))
        #Sat_pos_y
        a.append(round(random.randint(0,10)))
        # Velocidad Autogiro 
        a.append(round(0))
        # Estado del Software
        a.append("BOOT")
        #Latitud_2
        a.append(round(random.uniform(19.331,19.332),4))
        #Longitud
        a.append(- round(random.uniform(99.193,99.195),4))
        #Altitud_2
        if i*60 + j < 20*60: 
            a.append(0)
        elif 20*60 <= i*60 + j and i*60 + j < 30*60:
            a.append(round(subir[i*60 + j],1))
        elif 30*60 <= i*60 + j and i*60 + j < 37*60: 
            a.append(round(bajar[i*60 + j],1))
        elif 37*60 <= i*60 + j and i*60 + j <62*60: 
            print(i*60 + j, x[i*60 + j], vel_const[i*60 + j])
            a.append(round(vel_const[i*60 + j],1))
        else: 
            a.append(0)
        df.loc[len(df.index)] = a 
        a = [] 

df.to_csv("Datos_mis_simul.csv", header = False, index=False)
