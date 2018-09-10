#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:50:45 2017

@author: giacomo
"""
def DistPlan(df_coord_zero, l_allin):
    
    import math
    
    d_2_1=[]
    
    for i in range(0,len(l_allin)-1):    
        coord_E_1 = df_coord_zero.loc[l_allin[i]].coord_E
        coord_E_2 = df_coord_zero.loc[l_allin[i+1]].coord_E
        coord_N_1 = df_coord_zero.loc[l_allin[i]].coord_N
        coord_N_2 = df_coord_zero.loc[l_allin[i+1]].coord_N
        d_2_1.append(math.sqrt((coord_E_2-coord_E_1)**2+(coord_N_2-coord_N_1)**2))   
    # calcolo distanze cumulate per asse x grafico
    d_cum = [0]
    for i in range(0,len(d_2_1)):
        d_cum.append(d_cum[i]+d_2_1[i])
    
    return d_cum