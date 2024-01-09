#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

# Genera un csv de prueba para guardarlo y simular la recepción de datos de la telemetría de la misión. 

import pandas as pd 
import random 

df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'AltitudGPS':[],'GPS SATS':[],'Sat_pos_x':[],'Sat_pos_y':[],'Autogiro_vel':[],'Estado Software':[]})

a = []

for i in range(0,100): 
    #ID
    a.append("#ORB")
    #Time
    if i < 10: 
        a.append(f'0:00:0{i}')
    elif 10 <= i and i <60: 
        a.append(f'0:00:{i}')
    elif 60 <= i: 
        a.append(f'0:01:0{i-60}')
    #Packet Count
    a.append(i + 1)
    #Altitud
    if i < 20: 
        a.append(0)
    elif 20 <= i and i < 30:
        a.append(round(((9.81)*(i-20)**2)/2, 1))
        print(a)
    elif 30 <= i and i < 35: 
        a.append(round(((9.81)*(i-20)**2)/2 - ((9.81)*(i - 30)**2)/2,1))
    elif 35 <= i and i <35+20: 
        a.append(round(200 - (i-35)*10,1))
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
    elif 60 <= i: 
        a.append(f'11:30:0{i-60}')
    #Latitud
    a.append(round(random.uniform(18,19),4))
    #Longitud
    a.append(round(random.uniform(99,100),4))
    #Altitud GPS
    if i < 20: 
        a.append(2240)
    elif 20 <= i and i < 30:
        a.append(round(2240 + ((9.81)*(i-20)**2)/2, 1))
    elif 30 <= i and i < 35: 
        a.append(round(2240 + ((9.81)*(i-20)**2)/2 - ((9.81)*(i - 30)**2)/2,1))
    elif 35 <= i and i <35+20: 
        a.append(round(2240 + 200 - (i-35)*10,1))
    else: 
        a.append(2240)
    #GPS SATS
    a.append(1)
    #Sat_pos_x
    a.append(round(random.randint(0,10)))
    #Sat_pos_y
    a.append(round(random.randint(0,10)))
    # Velocidad Autogiro 
    a.append(round(0))
    # Estado del Software
    a.append("BOOT")
    df.loc[len(df.index)] = a 
    a = []

df.to_csv("Datos_mis_simul.csv", header = False, index=False)
