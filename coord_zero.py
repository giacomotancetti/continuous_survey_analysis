#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:26:22 2017

@author: giacomo tancetti

Function "CoordZero" returns DataFrame "df_coord_zero" containing the
zero-coordinates of each point.

Note: zero-coordinates are obtained by meaninig the coordinates measured during
the first day of measurements available.
"""

import pandas as pd

def CoordZero(pts_names,df_coord):
    
    # finding the first measurement date of each point and create the
    # dictionary "d_data_zero{keys:values}" where keys are points names and
    # values are the first measurement dates in chronological order.
    d_data_zero={}
    l_date_zero=[]
       
    for pt in pts_names:
        # finding the first date in chronological order
        date_misu = df_coord.time.loc[pt]
        date_misu.sort_values(inplace=True)
        l_date_zero.append(date_misu.iloc[0].date())
    
    d_data_zero=dict(zip(pts_names, l_date_zero))

    df_coord_zero = pd.DataFrame(columns=["time","E","N","H","dev_st_E","dev_st_N","dev_st_H"])

    nome_pt=[]
    l_E_zero=[]
    l_N_zero=[]
    l_H_zero=[]
    l_sE_zero=[]
    l_sN_zero=[]
    l_sH_zero=[]
    data_misu_zero=[]
    
    # for cycle constructs for each point list variables of all measures in
    # order to calculate mean values during the first day of observations.
    # Calculated mean values are the grouped in dictionary "d_coord_zero".
    for pt in pts_names:
        E_list = []
        N_list = []
        H_list = []
        sE_pt_list = []
        sN_pt_list = []
        sH_pt_list =[]
        
        df_coord_pto = df_coord.loc[pt]
        
        for index,row in df_coord_pto.iterrows():
            if row.time.date() == d_data_zero[pt]:
                E_list.append(row.E)
                N_list.append(row.N)
                H_list.append(row.H)
                sE_pt_list.append(row.dev_st_E)
                sN_pt_list.append(row.dev_st_N)
                sH_pt_list.append(row.dev_st_H)

        # calculating mean values and creating auxiliary dictionary variable
        # "d_coord_zero" to DataFrame "df_coord_zero"
        nome_pt.append(pt)
        l_E_zero.append(sum(E_list)/len(E_list))
        l_N_zero.append(sum(N_list)/len(N_list))
        l_H_zero.append(sum(H_list)/len(H_list))
        l_sE_zero.append(sum(sE_pt_list)/len(sE_pt_list))
        l_sN_zero.append(sum(sN_pt_list)/len(sN_pt_list))
        l_sH_zero.append(sum(sH_pt_list)/len(sH_pt_list))
        data_misu_zero.append(d_data_zero[pt])
        
        d_coord_zero = {"points_names":pt,"E":l_E_zero,"N":l_N_zero,"H":l_H_zero,"dev_st_E":l_sE_zero,"dev_st_N":l_sN_zero,"dev_st_H":l_sH_zero,"time":data_misu_zero}

    # creating DataFrame variable "df_coord_zero"
    df_coord_zero = pd.DataFrame(d_coord_zero,columns=["time","E","N","H","dev_st_E","dev_st_N","dev_st_H"],index =pts_names)
    
    return df_coord_zero