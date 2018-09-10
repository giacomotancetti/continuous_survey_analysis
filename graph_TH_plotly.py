#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:38:47 2017

@author: giacomo
"""

import plotly
import plotly.graph_objs as go
import copy

def GraphTHPlotly(df_delta, pts_names):
    # inizializzazione variabili
    traces=[]
    l_visible=[False for i in range(0,len(pts_names))]
    l_buttons=[]
    i=0
    # per ogni punto misurato vengono presi i dati da graficare dalla variabile
    # di tipo DataFrame 'df_delta'
    for nome_pto in pts_names:
        # definizione 'traces' da rappresentare in asse x e y
        traces.append(plotly.graph_objs.Scatter(
                x = df_delta.loc[nome_pto].time,
                y = df_delta.loc[nome_pto].H,
                mode = 'lines',
                # nome della serie di dati
                name = nome_pto
                    )
                )
    
        # definizione del menù a tendina per la selezione della serie da rappresentare
        # nella posizione i-esima della lista 'l_visible_i' viene scritto True
        l_visible_i=copy.deepcopy(l_visible)
        l_visible_i[i]=True
                   
        l_buttons.append({
          "args": ["visible", l_visible_i], 
          "label": nome_pto, 
          "method": "restyle"
          })
        
        i=i+1
        
    data = go.Data(traces)
    # definizione delle caratteristiche dell'asse y
    yaxis_par=dict(title='delta H [m]',
                   titlefont=dict(family='Arial', size=12, color='black'),
                   showticklabels=True,
                   tickangle=0,
                   tickfont=dict(family='Arial',size=12,color='black'),
                   range=[-0.04, 0.04])
    # impostazione del layout del grafico
    layout={'title':'Grafico delta H STZ004',
            'yaxis': yaxis_par,
            'updatemenus':[{'x':-0.05,'y':1,'yanchor':'top','buttons':l_buttons}]
            }
            
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig,filename='graph_TH.html')