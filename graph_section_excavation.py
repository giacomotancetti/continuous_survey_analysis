#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:17:39 2018

@author: giacomo
"""

import pandas as pd
from datetime import datetime
import plotly
import plotly.graph_objs as go

pk_section=5273  # pk della sezione da graficare
num_an=10        # numero degli avanzamenti da analizzare prima e dopo la sezione

# lettura del file contenente i dati Tempo-progressiva stazione-n° anello-
# progressiva fronte di scavo
df_pk=pd.read_csv("avanzamento_scavo.csv")
df_pk=df_pk.rename(index=str,columns={"Timestamp":"Tempo"})

# find the nearest value of the pk in df_pk DataFrame
pkInDf=min(df_pk['Progressiva'], key=lambda x:abs(x-pk_section))
baseIndex=int(df_pk[df_pk['Progressiva']==pkInDf].Station.index[0])

l_times=[]
l_pk=[]

for i in range(baseIndex-10,baseIndex+10):
    l_times.append(datetime.strptime(df_pk.iloc[i].Tempo,"%Y-%m-%d %H:%M"))
    l_pk.append(df_pk.iloc[i].Progressiva)
    
    
def GraphSecExPlotly(df_delta, l_times,l_pk, d_cum, l_allin):
    
    traces=[]
    
    for i in range(0,len(l_times)):
    
        c_E_pt_delta=[]
        c_N_pt_delta=[]
        c_H_pt_delta=[]
        
        # assegnazione della data i-esima alla variabile data_misu_an
        data_misu_an = l_times[i]
        dist_rel=l_pk[i]-pk_section

        # individuazione DataFrame df_delta_i dei valori delta calcolati nella data i-esima
        time_i=min(df_delta['time'], key=lambda x:abs(x-data_misu_an))
        df_delta_i=df_delta.loc[(df_delta.time==time_i)]

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

        # creazione delle variabili tipo list ausiliarie alla costruzione della
        # variabile "d_delta_i_pto" 
            df_delta_i_pto = df_delta_i.loc[nome_pti_i_allin[j]]
            c_E_pt_delta.append(df_delta_i_pto.E)
            c_N_pt_delta.append(df_delta_i_pto.N)
            c_H_pt_delta.append(df_delta_i_pto.H)
               
            d_delta_i_pto = {"dist_fronte_sez":dist_rel,"E":c_E_pt_delta,"N":c_N_pt_delta,"H":c_H_pt_delta}
    
        # creazione della variabile tipo DataFrame "df_delta_graph_i"
        df_delta_graph_i = pd.DataFrame(d_delta_i_pto,columns=["dist_fronte_sez","E","N","H"],index = nome_pti_i_allin)

        # stampa grafici delta H
        traces.append(plotly.graph_objs.Scatter(
                x = d_cum,
                y = df_delta_graph_i.H,
                mode = 'lines',
                # nome della serie di dati
                name = int(dist_rel)
                    )
                )
    
    data = go.Data(traces)
    
    # definizione delle caratteristiche dell'asse y
    yaxis_par=dict(title='delta H [m]',
                   titlefont=dict(family='Arial', size=12, color='black'),
                   showticklabels=True,
                   tickangle=0,
                   tickfont=dict(family='Arial',size=12,color='black'),
                   range=[-0.02, 0.02])
    # definizione delle caratteristiche dell'asse x
    xaxis_par=dict(title='nome punto',
                   titlefont=dict(family='Arial', size=12, color='black'),
                   showticklabels=True,
                   tickangle=0,
                   tickfont=dict(family='Arial',size=12,color='black'),
                   tickvals=d_cum,    # posizioni delle etichette dell'asse x mostrate
                   ticktext=l_allin   # definizione delle etichette dell'asse x
                   )
    # impostazione del layout del grafico
    layout={'title':'Grafico allineamento 1 STZ013',
            'yaxis': yaxis_par,
            'xaxis': xaxis_par,
            'updatemenus':[{'x':-0.05,'y':1,'yanchor':'top'}]
            }
            
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='graph_allin.html')