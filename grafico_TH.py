#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:05:15 2017

@author: giacomo
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

def GraficoTH(l_allin,df_delta):
    
    fig, axarr = plt.subplots(int(len(l_allin)/3), 3)
    mytitle= fig.suptitle('GALLERIA SANTA LUCIA - GRAFICO TEMPO - SPOSTAMENTI VERTICALI PUNTI ALLINEAMENTO 1 STZ003',
             fontsize=6, y=1.02)

    j = 0
    k = 0

    for i in range(0,len(l_allin)):
        # assegnazione alla variabile x della serie da usare come ascissa del grafico
        x = df_delta.loc[l_allin[i]].data_misura
        # assegnazione alla variabile y della serie da usare come ordinata del grafico
        y = df_delta.loc[l_allin[i]].quota.values
        # stampa grafico nella posizione j,k 
        axarr[j, k].plot(x, y, linewidth=0.5)
        # impostazione legenda
        axarr[j, k].legend((l_allin[i],),loc='upper left',fontsize=4,frameon=False,handlelength=1)
        # Set y limits
        axarr[j, k].set_ylim(-0.05, 0.05)
        # Impostazione dimensione caratteri assi
        axarr[j, k].tick_params(axis='both',labelsize=4,length=2,pad=0.5)
        axarr[j, k].xaxis_date()
        # Impostazione griglia
        axarr[j, k].grid(color='black', linestyle='-', linewidth=0.2)
        # Impostazione etichetta asse x
        axarr[j, k].set_xlabel('data', size = 4,labelpad=0.5)
        # Impostazione etichetta asse y
        axarr[j, k].set_ylabel('spostamenti [m]', size = 4,labelpad=0.5)
        # incremento indici di posizione j,k
        k = k+1
        if j>=len(l_allin)/3:
            j=0
        if k>=3:
            k=0
            j = j+1
        
        fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    fig.savefig('grafico.png', dpi=500, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches='tight', pad_inches=0.1,
                frameon=None, bbox_extra_artists=[mytitle])
    
    