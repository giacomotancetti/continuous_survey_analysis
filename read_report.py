#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 12:03:49 2017

@author: giacomo tancetti
"""
'''
ReadReport reads data from each file in the specified path and groups 
informations on DataFrame "df_coord"
'''
import pandas as pd
import os
import datetime

def ReadReport(path):

    df_coord = pd.DataFrame(columns=["time","E","N","H","dev_st_E","dev_st_N","dev_st_H"])
    df_list = []

    for filename in os.listdir(path):
        # opening files in path and reading every row.
        # In list "l_rows" each element is a row of the readed file
        f = open(path+filename,"r")        
        l_rows = f.readlines()       
        print(f)
        f.close()

        # reading measurements date as string "str_data_misu"
        riga_split = l_rows[2].split(' ')   
        str_data_misu = riga_split[3]
        # parsing string "str_data_misu" and get day, month, year of the
        # measurement
        n_pos = [pos for pos, char in enumerate(str_data_misu) if char == '/']
        day = int(str_data_misu[(n_pos[0]+1):n_pos[1]])
        month = int(str_data_misu[:n_pos[0]])
        year = int(str_data_misu[(n_pos[1]+1):])
        # reading measurements hh:mm:ss as string "hhmmss_str"
        hhmmss_str = riga_split[4]
        period = riga_split[5][:2]
        # parsing "hhmmss_str" and get hour, minutes, seconds of the 
        # measurement
        n_pos = [pos for pos, char in enumerate(hhmmss_str) if char == ':']
        hour_12_str = hhmmss_str[:n_pos[0]]
        # converting from 12-hours clock format to 24-hours clock format
        if period == 'AM' and hour_12_str !='12':
            hour = int(hour_12_str)
        elif period == 'AM' and hour_12_str =='12':
            hour = int(0)
        elif period == 'PM' and hour_12_str !='12':
            hour = int(hour_12_str)+12
        elif period == 'PM' and hour_12_str == '12':
            hour = int(hour_12_str)
        else:
            print('Period AM or PM indication error')         
        
        minutes = int(hhmmss_str[(n_pos[0]+1):n_pos[1]])
        sec = int(hhmmss_str[-2:])

        # assembling year,month,day,hour,minutes,sec into datetime variable 
        # "data_misu_i"
        data_misu_i = datetime.datetime(year,month,day,hour,minutes,sec)

        # finding in "l_rows" list the position of  points coordinates using
        # 'PtNr' marker
        pos_PtNr = [i for i, s in enumerate(l_rows) if 'PtNr' in s]
        pos_coord_misu = pos_PtNr[len(pos_PtNr)-1]+2
                          
        pts_names=[]
        E_pt=[]
        N_pt=[]
        H_pt=[]
        sE_pt=[]
        sN_pt=[]
        sH_pt=[]
        data_misu=[]

        # creating lists points names(pts_names), east coordinate (E_pt), 
        # north coordinate (N_pt), H (H_pt), dev. standard coord est (sE_pt)
        # dev. standard coord nord (sN_pt), dev. standard H (sH_pt)
        for i in range(pos_coord_misu,len(l_rows)-1):
            riga_split = l_rows[i].split(' ')
            riga_split = [l for l in riga_split if l != ''] # removing empty elements
            riga_split[len(riga_split)-1] = riga_split[len(riga_split)-1].replace('\r\n','')# removing end of line character

            pts_names.append(riga_split[0])
            E_pt.append(float(riga_split[1]))
            N_pt.append(float(riga_split[2]))
            H_pt.append(float(riga_split[3]))
            sE_pt.append(float(riga_split[4]))
            sN_pt.append(float(riga_split[5]))
            sH_pt.append(float(riga_split[6]))
            data_misu.append(data_misu_i)
            data_dict = {"points_names":pts_names,"E":E_pt,"N":N_pt,"H":H_pt,"dev_st_E":sE_pt,"dev_st_N":sN_pt,"dev_st_H":sH_pt,"time":data_misu}

        # creation variable df_coord_i 
        df_coord_i = pd.DataFrame(data_dict,columns=["time","E","N","H","dev_st_E","dev_st_N","dev_st_H"],index =pts_names)
        df_list.append(df_coord_i)
        df_coord=pd.concat(df_list)
    # sorting DataFrame by measurement date
    df_coord = df_coord.sort_values('time')
    
    return df_coord
    