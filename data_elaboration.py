#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 10:17:30 2018

@author: giacomo
"""

import pandas as pd
from scipy import stats
import statsmodels.api as sm

def LinReg(df_coord,startDate,endDate):
    d_coeffRetta={} 
    for pt in df_coord.index.unique():
        y=df_coord[(df_coord['time']>=startDate)&(df_coord['time']<=endDate)]['H'].loc[pt].values
        x1=df_coord[(df_coord['time']>=startDate)&(df_coord['time']<=endDate)]['time'].loc[pt]
        t0=x1.iloc[0]
        x=[]
        for t1 in x1:
            x.append((t1-t0).total_seconds())
        
        m=stats.linregress(x,y)[0]
        d_coeffRetta[pt]=m
            
        df_coeffRetta= pd.DataFrame.from_dict(d_coeffRetta,orient='index')
        df_coeffRetta.columns=['m']
    return(df_coeffRetta)
        

def DelTrend(df_coord,startDate,endDate):
 
    deltaT=(endDate-startDate).total_seconds()
    x1=0
    x2=deltaT
    
    df_coeffRetta=LinReg(df_coord,startDate,endDate)
    
    df_coord_mod=df_coord.copy()
    
    for pt in df_coord.index.unique():
        m_i=df_coeffRetta['m'].loc[pt]
        t0=df_coord['time'].loc[pt].iloc[0]
        s_t_misu=df_coord['time'].loc[pt]
        decomp = sm.tsa.seasonal_decompose(df_coord.loc[pt].H, model='additive',freq=24)
        seasonal=decomp.seasonal.tolist()    
        l_delta_t=[]
        for t in s_t_misu:
            l_delta_t.append((t-t0).total_seconds())
        
        l_delta_s=[x*m_i for x in l_delta_t]
        
        l_quote_dep=(df_coord['H'].loc[pt]-l_delta_s-seasonal).tolist()
        
        df_coord_mod['H'].loc[pt]=l_quote_dep
        
    return(df_coord_mod)


