#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 18:25:40 2022

@author: camrit
"""
import pandas as pd
import geopandas as gpd
import geoplot as gplt
import os.path
import geoplot.crs as gcrs
import numpy as np
#import cv2

def stringSplit(admin2Regions):
    admin2RegionList = admin2Regions.split('/')
    return admin2RegionList

#reading file using absolute path - my_path is where this file is!
my_path = os.path.abspath(os.path.dirname(__file__))
# Mao of the Sahel Region - Admin2
path0 = os.path.join(my_path, "sah_admin0_ocha/sah_admin0_ocha.shp")
# Mao of the Sahel Region - Admin2
path2 = os.path.join(my_path, "sah_admin2/sah_admin2.shp")

#Showing Sahel map
#img = cv2.imread('countries-sahel.png',0)
#cv2.imshow('image',img)
#path1 = os.path.join(my_path, "africa-places-shape/places.shp")
sh_df0 = gpd.read_file(path0)
#We first display the Sahel countries
ax= sh_df0.plot(edgecolor='black', cmap='Greys', legend=True, figsize=(50, 25))
#Get the labels
#label = sh_df0.admin0Name
#ax.annotate(label, xytext=(3, 3), textcoords="offset points")

#print(path)
sh_df = gpd.read_file(path2)
#africa_df= gpd.read_file(path1)

#We have 3 year's data
yearList = ['2020', '2021', '2022']

#reading file in the local directory
sahel_data = gpd.read_file('2022_2020_Revised_V2.csv')
#sahel_data = pd.read_excel('2020to2022_country_burdens_prevalences_are_merged__updated.xlsx')

#There are some rows with 'High' and not 'HIGH' - converting everything to capitals
sahel_data['priority level validated by the clusters'] = sahel_data['priority level validated by the clusters'].str.upper()

 #Converting the categorical column into Ordinal column names 'target'
sahel_data['target'] = sahel_data['priority level validated by the clusters'].factorize(['low', 'medium', 'high', 'very high'])[0]
"""
Alterative to the above:
sahel_data['priority level validated by the clusters'] = sahel_data['priority level validated by the clusters'].astype('category')
sahel_data['target'] = sahel_data['priority level validated by the clusters'].cat.codes 
"""
for year in yearList:
   #Creating a new dataframe with only the interesting values
   #df2020 = sahel_data[sahel_data['year']=='2020'][['country','population_totale', 'admin1', 'admin2_sanitary' ]]
   #df2020['target'] = sahel_data[sahel_data['year']=='2020']['priority level validated by the clusters'].factorize(['low', 'medium', 'high', 'very high'])[0]

    # Now we try to do this: sh_df['target'] = np.where(df2020['admin2_sanitary']==sh_df['admin2Name'], df2020['target'], 0)
    sh_df['target']= np.nan

    for index, row in sh_df.iterrows():
        for index1, row1 in sahel_data[sahel_data['year']==year].iterrows():
            if (row['admin2Name']==row1['ADMIN 2 Admnistratif']) or (any(elem == row['admin2Name'] for elem in stringSplit(row1['admin2_sanitary']))) or  (any(elem == row['admin2Name'] for elem in stringSplit(row1['DS/ADMIN 2 Admnistratif (Burden Data)']))) :
                sh_df.at[index,'target']=row1['target']
    
    missing_kwds = dict(color='lightgrey')
    
    ax = sh_df.plot(column='target', cmap='OrRd',  edgecolor='black', legend=True, missing_kwds=missing_kwds, figsize=(50, 25))
    fig = ax.figure
    cb_ax =fig.axes[1]
    cb_ax.tick_params(labelsize=40)

"""
    gplt.choropleth(
        sh_df, hue='target', projection=gcrs.AlbersEqualArea(),
        edgecolor='black', linewidth=1,
        cmap='OrRd', legend=True,
        scheme='FisherJenks',
        figsize=(20, 10),
        legend_labels=[
             'low', 'medium', 'high', 'very high'
            ]
        )

    This is for the larger African map
    
    africa_df['target']=0

    for index, row in africa_df.iterrows():
        for index1, row1 in sahel_data[sahel_data['year']==year].iterrows():
            if (row['name']==row1['admin2_sanitary']):
                africa_df.at[index,'target']=row1['target']
    gplt.choropleth(
     africa_df, hue='target', projection=gcrs.AlbersEqualArea(),
     edgecolor='black', linewidth=1,
     cmap='OrRd', legend=False,
     scheme='FisherJenks',
     
     )           
"""

     

