#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Wed  27 22:30:20 2018

@author: giacomo tancetti
"""

import datetime

from read_report import ReadReport
from coord_zero import CoordZero
from calc_delta_v3 import CalcDelta_v3
from dist_plan import DistPlan
from grafico_allin import GraficoAllin
from grafico_TH import GraficoTH
from contour import Contour
from graph_TH_plotly import GraphTHPlotly
from grafico_allin_plotly import GraphAllPlotly
from data_elaboration import DelTrend

# directory containing report files
path = "./report_STZ013/"

# DataFrame "df_coord" contains data read from reports contained in path directory
df_coord = ReadReport(path)

# save DataFrame "df_coord" in memory
#df_coord.to_pickle('df_coord.p')

# read DataFrame "df_coord" from memory
#df_coord = pd.read_pickle('df_coord.p')

# list of the names of the points measured at least one time 
pts_names = df_coord.index.unique().tolist()
pts_names.sort()

# "df_coord_zero" contains the points zero-cooordinates
df_coord_zero = CoordZero(pts_names,df_coord)

# remove from H coordinates trend independent from tunnel excavation.
# Reference start and end dates must be declared in the module
startDate=datetime.date(year=2018,month=7,day=1)
endDate=datetime.date(year=2018,month=7,day=13)
df_coord_mod= DelTrend(df_coord,startDate,endDate)

# calculate the displacements between points zero coordinates and t-time
# coordinates
#df_delta = CalcDelta_v3(df_coord_mod,df_coord_zero,pts_names)
df_delta = CalcDelta_v3(df_coord,df_coord_zero,pts_names)

# define the points list of the analyzed alignment 
l_allin = ['013001','013002','013003','013004','013005','013006','013007','013008']

# calculate the mutual distances between points of the analyzed alignment
#d_cum = DistPlan(df_coord_zero,l_allin)

# define list of dates to rapresent in the graphs
l_data_misu_an = ['08/07/2018','09/07/2018','10/07/2018','11/07/2018',
                  '12/07/2018','13/07/2018','14/07/2018','15/07/2018',
                  '16/07/2018','17/07/2018','18/07/2018','19/07/2018',
                  '20/07/2018','21/07/2018']

# print graph point names - H displacements using matplotlib
#GraficoAllin(df_delta, l_data_misu_an, d_cum, l_allin)

# print graph point names - H displacements using plotly
#GraphAllPlotly(df_delta, l_data_misu_an, d_cum, l_allin)

# print graph time - H displacements unsing matplotlib
#GraficoTH(l_allin,df_delta)

# print graph time - H displacements unsing plotly
GraphTHPlotly(df_delta,pts_names)

# print contour graph
#Contour(pts_names,df_coord_zero,df_delta,l_data_misu_an)
