#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

# Genera un csv de prueba para guardarlo y simular la recepción de datos de la telemetría de la misión. 

import pandas as pd 
import random 

df = pd.DataFrame({'ID':[],'Mission Time':[],'Packet Count':[],'Altitud':[],'Presión':[],'Temperatura':[],'Voltaje':[],'Hora':[],'Latitud':[],'Longitud':[],'AltitudGPS':[],'GPS SATS':[],'Sat_pos_x':[],'Sat_pos_y':[],'Autogiro_vel':[],'Estado Software':[]})

a = []

for i in range(0,100): 
    for j in range(0,59): 

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
            a.append(f'0:02:{i-60}')

        #Packet Count
        a.append(i*60 + j + 1)
        
        #Altitud
        if j == 0: 
            if i < 20: 
                a.append(0)
            elif 20 <= i and i < 30:
                a.append(round(((9.81)*(i-20)**2)/2, 1))
            elif 30 <= i and i < 35: 
                a.append(round(((9.81)*(10)**2)/2 - (((9.81)*(i - 30)**2)/2),1))
            elif 35 <= i and i <35+20: 
                a.append(round(200 - (i-35)*10,1))
            else: 
                a.append(0)
        else:
            if i < 20: 
                a.append(0)
            elif 20 <= i and i < 30:
                a.append(round(((9.81)*(i-20 + 1/j)**2)/2, 1))
            elif 30 <= i and i + 1/j < 35: 
                a.append(round(((9.81)*(10)**2)/2 - (((9.81)*(i - 30 + 1/j)**2)/2),1))
            elif 35 <= i and i <35+20: 
                a.append(round(200 - (i-35 + 1/j)*10,1))
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
        a.append(round(random.uniform(19.30,19.35),4))
        #Longitud
        a.append(- round(random.uniform(99.15,99.20),4))
        #Altitud GPS
        if j == 0: 
            if i < 20: 
                a.append(2240)
            elif 20 <= i and i < 30:
                a.append(round(2240 +((9.81)*(i-20)**2)/2, 1))
            elif 30 <= i and i < 35: 
                a.append(round(2240 +((9.81)*(10)**2)/2 - (((9.81)*(i - 30)**2)/2),1))
            elif 35 <= i and i <35+20: 
                a.append(round(2240 + 200 - (i-35)*10,1))
            else: 
                a.append(0)
        else:
            if i < 20: 
                a.append(2240)
            elif 20 <= i and i < 30:
                a.append(round(2240 + ((9.81)*(i-20 + 1/j)**2)/2, 1))
            elif 30 <= i and i < 35: 
                a.append(round(2240 + ((9.81)*(10)**2)/2 - ((9.81)*(i - 30 + 1/j)**2)/2,1))
            elif 35 <= i and i <35+20: 
                a.append(round(2240 + 200 - (i-35 + 1 /j**2)*10,1))
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
