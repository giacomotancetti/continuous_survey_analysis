#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:01:05 2017

@author: giacomo tancetti

"""
import datetime
import pandas as pd
import plotly
import plotly.graph_objs as go

def GraphAllPlotly(df_delta, l_data_misu_an, d_cum, l_allin):
    
    traces=[]
    
    for i in range(0,len(l_data_misu_an)):
    
        c_E_pt_delta=[]
        c_N_pt_delta=[]
        c_H_pt_delta=[]
        data_misu_delta=[]
        
        # assegnazione della data i-esima alla variabile data_misu_an
        data_misu_an = l_data_misu_an[i]
    
        # individuazione valori giorno, mese, anno nella stringa "data_misu_an"
        n_pos = [pos for pos, char in enumerate(data_misu_an) if char == '/']
        day = int(data_misu_an[:n_pos[0]])
        month = int(data_misu_an[(n_pos[0]+1):n_pos[1]])    
        year = int(data_misu_an[(n_pos[1]+1):])

        # individuazione DataFrame dei valori delta calcolati nella data i-esima
        d=datetime.timedelta(days=1)
        df_delta_i=df_delta.loc[(df_delta.time>datetime.datetime(year,month,day)) & (df_delta.time<(datetime.datetime(year,month,day))+d)]

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
            data_misu_delta.append(datetime.datetime(year,month,day))
        
            # creazione delle variabili tipo list ausiliarie alla costruzione della
            # variabile "d_delta_i_pto"        
            d_delta_i_pto = {"time":data_misu_delta,"E":c_E_pt_delta,"N":c_N_pt_delta,"H":c_H_pt_delta}
    
        # creazione della variabile tipo DataFrame "df_delta_graph_i"
        df_delta_graph_i = pd.DataFrame(d_delta_i_pto,columns=["time","E","N","H"],index = nome_pti_i_allin)

        # stampa grafici delta H
        traces.append(plotly.graph_objs.Scatter(
                x = d_cum,
                y = df_delta_graph_i.H,
                mode = 'lines',
                # nome della serie di dati
                name = datetime.datetime(year,month,day)
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
