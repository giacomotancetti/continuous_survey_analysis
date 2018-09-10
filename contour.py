#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 15:53:34 2017

@author: giacomo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import scipy.interpolate
from scipy.misc import imread
import datetime
import pandas as pd

def Contour(pts_names,df_coord_zero,df_delta,l_data_misu_an):
    
    # eliminazione pti CSD dalla lista dei punti graficati
    pts_names_cont=[i for i in pts_names if 'CSD' not in i]
        
    for data_misu_an in l_data_misu_an:
        
        l_delta_h=[]
        l_E=[]
        l_N=[]
        
        # individuazione valori giorno, mese, anno nella stringa "data_misu_an"
        n_pos = [pos for pos, char in enumerate(data_misu_an) if char == '/']
        
        day = int(data_misu_an[:n_pos[0]])
        month = int(data_misu_an[(n_pos[0]+1):n_pos[1]])    
        year = int(data_misu_an[(n_pos[1]+1):])
        
        # data in formato 'datetime'
        data_an=datetime.datetime(year,month,day)
   
        for nome_punto in pts_names_cont:
            E=df_coord_zero.loc[nome_punto].coord_E
            N=df_coord_zero.loc[nome_punto].coord_N
            d=datetime.timedelta(days=1)
            delta_h=df_delta.quota[(df_delta['data_misura']>data_an) & 
                                   (df_delta['data_misura']<data_an+d)].loc[nome_punto].mean()
            l_E.append(E)
            l_N.append(N)
            l_delta_h.append(delta_h)
        
            d_dati_cont={"coord_E":l_E,"coord_N":l_N,"delta_h":l_delta_h}
        
        df_dati_cont=pd.DataFrame(d_dati_cont,columns=["coord_E","coord_N","delta_h"],index =pts_names_cont)
    
        # Set up a regular grid of interpolation points
        xi, yi = np.linspace(df_dati_cont.coord_E.min(), df_dati_cont.coord_E.max(), 500), np.linspace(df_dati_cont.coord_N.min(), df_dati_cont.coord_N.max(), 500)
        xi, yi = np.meshgrid(xi, yi)
    
        # Interpolate
        rbf = scipy.interpolate.Rbf(df_dati_cont.coord_E, df_dati_cont.coord_N, df_dati_cont.delta_h, function='linear')
        zi = rbf(xi, yi)
    
        fig, ax = plt.subplots()
        
        cont=ax.imshow(zi, vmin=-0.02, vmax=0.02, origin='lower',
                       extent=[df_dati_cont.coord_E.min(), df_dati_cont.coord_E.max(), df_dati_cont.coord_N.min(), df_dati_cont.coord_N.max()])
        #ax.contourf(xi,yi,zi,cmap=plt.cm.jet)    
        ax.set_xlim(df_dati_cont.coord_E.min(), df_dati_cont.coord_E.max())
        ax.set_ylim(df_dati_cont.coord_N.min(), df_dati_cont.coord_N.max())
        ax.set(title=data_an.date(),xlabel='coord E', ylabel='coord N')
        ax.tick_params(axis='x',direction='out',labelsize=6, length=1, width=1, colors='black',pad=1)
        ax.tick_params(axis='y',direction='out',labelsize=6, length=1, width=1, colors='black',pad=1)
        ax.set_aspect('equal')
        majorFormatter = FormatStrFormatter('%8.0f')
        ax.xaxis.set_major_formatter(majorFormatter)
        ax.yaxis.set_major_formatter(majorFormatter)
        cbar = fig.colorbar(cont, ticks=[-0.02,-0.01,0.0,0.01, 0.02])
        cbar.ax.set_yticklabels(['-0.02','-0.01','0.0','0.01','0.02'])
        cbar.ax.tick_params(axis='y',direction='out',labelsize=6, length=1, width=1, colors='black',pad=1)
        cbar.ax.set(ylabel='spostamenti vert [m]')
        
        img = imread('image.png')
        ax.imshow(img,zorder=1,alpha=0.1,extent=[df_dati_cont.coord_E.min(), df_dati_cont.coord_E.max(), df_dati_cont.coord_N.min(), df_dati_cont.coord_N.max()])

        '''
        fig.savefig(str(data_an.date())+'.png', dpi=600.0, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches='tight', pad_inches=0.1,
                    frameon=None)'''