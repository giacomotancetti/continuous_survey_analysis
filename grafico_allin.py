#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:01:05 2017

@author: giacomo tancetti

"""

def GraficoAllin(df_delta, l_data_misu_an, d_cum, l_allin):
    
    import datetime
    import pandas as pd
    import matplotlib.pyplot as plt

    for i in range(0,len(l_data_misu_an)):
    
        c_E_pt_delta=[]
        c_N_pt_delta=[]
        c_H_pt_delta=[]
        
        # assegnazione della data i-esima alla variabile data_misu_an
        data_misu_an = l_data_misu_an[i]
    
        # individuazione valori giorno, mese, anno nella stringa "data_misu_an"
        n_pos = [pos for pos, char in enumerate(data_misu_an) if char == '/']
        day = int(data_misu_an[:n_pos[0]])
        month = int(data_misu_an[(n_pos[0]+1):n_pos[1]])    
        year = int(data_misu_an[(n_pos[1]+1):])

        # individuazione DataFrame dei valori delta calcolati nella data i-esima
        d=datetime.timedelta(days=1)
        df_delta_i=df_delta.loc[(df_delta.data_misura>datetime.datetime(year,month,day)) & (df_delta.data_misura<(datetime.datetime(year,month,day))+d)]

        # inizializzazione lista "nome_pti_i" contenente i nomi di tutti i punti misurati nella data i-esima
        nome_pti_i = []
        # inizializzazione lista "nome_pti_i_allin" contenente i nomi di tutti i punti misurati nella data i-esima appartenenti alla lista "l_allin"
        nome_pti_i_allin = []
        for k in range(0,len(df_delta_i.index)):
            if df_delta_i.index[k] not in nome_pti_i:
                nome_pti_i.append(df_delta_i.index[k])
                nome_pti_i.sort()
        # creazione lista "nome_pti_i_allin" contenente i nomi di tutti i punti misurati nella data i-esima appartenenti alla lista "l_allin"
        for n in nome_pti_i:
            if n in l_allin:
                nome_pti_i_allin.append(n)
        
        for j in range(0,len(nome_pti_i_allin)):
               
            df_delta_i_pto = df_delta_i.loc[nome_pti_i_allin[j]]
            df_delta_i_pto_mean = df_delta_i_pto.mean()
            c_E_pt_delta.append(df_delta_i_pto_mean[0])
            c_N_pt_delta.append(df_delta_i_pto_mean[1])
            c_H_pt_delta.append(df_delta_i_pto_mean[2])     
        
            # creazione delle variabili tipo list ausiliarie alla costruzione della
            # variabile "d_delta_i_pto"        
            d_delta_i_pto = {"nome_punto":nome_pti_i_allin,"coord_E":c_E_pt_delta,"coord_N":c_N_pt_delta,"quota":c_H_pt_delta}
    
        # creazione della variabile tipo DataFrame "df_delta_graph_i"
        df_delta_graph_i = pd.DataFrame(d_delta_i_pto,columns=["nome_punto","coord_E","coord_N","quota"],index = nome_pti_i_allin)

        # stampa grafici delta quota
        serie = plt.plot(d_cum,df_delta_graph_i.quota)
        plt.setp(serie,  linewidth=1.0)
        plt.axis([0,9,-0.02,0.005])
        plt.title('GALLERIA SANTA LUCIA - GRAFICO SPOSTAMENTI VERTICALI ALLINEAMENTO 2 STZ004', size=8)
        plt.xlabel('nome punto')
        plt.xticks(d_cum, l_allin, rotation='vertical')
        plt.ylabel('Delta quota [m]')
        plt.legend(l_data_misu_an,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
        plt.grid(color='black', linestyle='--', linewidth=0.5)

        plt.savefig('graph.png', dpi=600.0, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches='tight', pad_inches=0.2,
                    frameon=None)
