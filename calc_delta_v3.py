#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 22:36:25 2017

@author: giacomo
"""

import pandas as pd

def CalcDelta_v3(df_coord,df_coord_zero,pts_names):
    
    # inizializzazione variabili
    df_delta_v3 = pd.DataFrame(columns=["E","N","H"])
    
    # lettura dei dati contenuti nella variabile DataFrame "df_coord"
    for nome_pto in pts_names:
        # lettura della data della misura
        s_data_misu = df_coord.time.loc[nome_pto]
        # organizzazione delle coordinate del punto 'nome_pto' nella variabile di tipo Series
        s_coord = df_coord[['E','N','H']].loc[nome_pto]
        # organizzazione delle coordinate di zero del punto i-esimo nella variabile di tipo Series
        s_coord_zero = df_coord_zero[['E','N','H',]].loc[nome_pto]
        # calcolo delta coordinate
        delta_coord =  s_coord - s_coord_zero
        # aggiunta della colonna 'time' al DataFrame
        delta_coord['time']= s_data_misu
        # aggiunta alla variabile DataFrame "df_delta_v3" dei delta-coordinate del punto i-esimo
        df_delta_v3 = df_delta_v3.append(delta_coord)
    
    return df_delta_v3