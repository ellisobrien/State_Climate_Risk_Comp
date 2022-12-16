#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 11:39:38 2022

@author: ellisobrien
"""

#data processing and manipulatation packages
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

#visualization packages
import plotly.express as px
import plotly 

#dashboard package
import streamlit as st

#Writing dashboard title 
st.title("Comparing Natural Disaster and Climate Risk across California, Florida, Texas, and New York")

#Adding in authors name 
st.subheader('Ellis Obrien')

#Adding text describing issue 
st.markdown('_Natural disasters present a fundamental risk to housing and economic security in the U.S. In 2021 alone, natural disasters cost the U.S $145 Billion. In an effort to improve data surrounding natural disasters, the Federal Emergency Management Agency released the National Risk Index (NRI) which provides comprehensive county level data on natural disaster risks._')

st.markdown('_This dashboard uses NRI data to analyze and visualize climate risk in four states: California, Florida, New York and Texas. These states represent the four most populous states in the country and the four states with over 2 trillion dollars in building value. Additionally, California, Texas, and Florida represent the three states with the highest expected annual loss due to climate change. Analyzing these states allows us to see the risk profile of four distinct regions in the country._')


#imporing json 
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    county = json.load(response)
    
#importing data from github
NRI=pd.read_csv('https://raw.githubusercontent.com/ellisobrien/State_Climate_Risk_Comp/main/NRI_State_Dat.csv', dtype={"STCOFIPS": str})

NRI.rename(columns={'STCOFIPS':'FIPS'}, inplace=True)




##############################################################################
#section 1
##############################################################################
st.subheader('Overview of Loss by State and County Risk')



nri_plot_1=NRI[['STATEABBRV', 'EAL_VALB', "EAL_VALA", "EAL_VALPE"]]
nri_plot_1=nri_plot_1.groupby('STATEABBRV').sum()


nri_plot_1.reset_index(inplace=True)

nri_plot_1=nri_plot_1.sort_values(by=['EAL_VALB'], ascending=False)




nri_plot_1.rename(columns={'EAL_VALB': 'Building Loss',
                         'EAL_VALA': 'Agricultural Loss',
                         'EAL_VALPE': 'Population Loss'},
                                           inplace=True)

fig0 = px.bar(nri_plot_1, x="STATEABBRV", 
             y=['Building Loss', 'Agricultural Loss', 'Population Loss'], 
             title=("<b>Figure 1: Breakdown of Annual Expected Loss by State </b>"),
             labels={"value": "Annual Estimated Loss ($)", 'STATEABBRV':'State', "variable": "Loss Breakdown"},
             color_discrete_map={"Building Loss": "silver", "Agricultural Loss": "green", 'Population Loss':'black'},
             template="simple_white",
             height=400)
#displaying viz
st.plotly_chart(fig0)



State_Name1=st.selectbox(label="Select state to View",
options=('CA', 'FL', 'NY', 'TX' ))

title_text = "**" + State_Name1 + "**"



if State_Name1 == 'CA':
    x=38.1063
    y=-120.7367
    Map_Range2=(0,500000000)
    zoom=4.5
    
elif State_Name1 == 'FL':
    x= 28.9331
    y=-81.87650
    Map_Range2=(0,100000000)
    zoom=5
    
elif State_Name1 == 'NY':
    x= 42.9058
    y=-75.0933
    Map_Range2=(0,30000000)
    zoom=5
    
elif State_Name1 == 'TX':
    x=31.35394
    y=-99.25277
    Map_Range2=(0,50000000)
    zoom=4


NRI_MAP1=NRI[NRI.STATEABBRV == State_Name1]


#initilizing mapping function 
def county_map_1(input_var, map_leg, z, input_desc):
    fig1 = px.choropleth_mapbox(NRI_MAP1, geojson=county, locations='FIPS', color=input_var,
                                   color_continuous_scale="balance",
                                   range_color=map_leg,
                                   mapbox_style="carto-positron",
                                   zoom=z, center = {"lat": x, "lon": y},
                                   opacity=0.7,
                                   labels={input_var: input_desc, 'STCOFIPS':'FIPS'}
                                  )
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
    st.plotly_chart(fig1)


#writing map title 
st.write('**Figure 2: Annual Expected Loss for**', title_text, "**, by County**")

#Enter Variables to Map here 
variable_to_map_NRI2='EAL_VALT'

#Enter Variable Description 
NRI_description2='Annual Expected Loss'

county_map_1(variable_to_map_NRI2, Map_Range2, zoom, NRI_description2)

st.write('_Please note that the loss range changes for each state so that higher and lower loss counties can be differentiated between within a state._')


st.write('**Figure 3: Composite Risk Score for**', title_text, "**, by county**")
st.write('_Risk Score takes into account disaster threat, infrastructure, and building value to assign a risk rating to each county_')

#Enter Variables to Map here 
variable_to_map_NRI1='RISK_SCORE'

#Enter Variable Description 
NRI_description1='Composite Risk Score'

Map_Range1=(0,50)
#running mapping function
county_map_1(variable_to_map_NRI1, Map_Range1, zoom, NRI_description1)

#writing map title 2

##############################################################################
#section 2
##############################################################################
st.subheader('Analysis of Peril Specific Loss by State ')

State_Name2=st.selectbox(label="Select State",
options=('CA', 'FL', 'NY', 'TX' ))

title_text2 = "**" + State_Name2 + "**"

NRI_Map2=NRI[NRI.STATEABBRV == State_Name2]

NRI_Map2 = NRI_Map2.fillna(0)

NRI_Map2=NRI_Map2[['FIPS', 'AVLN_EALT',
'CFLD_EALT',
'CWAV_EALT',
'DRGT_EALT',
'ERQK_EALT',
'ISTM_EALT',
'HAIL_EALT',
'HWAV_EALT',
'HRCN_EALT',
'LTNG_EALT',
'LNDS_EALT',
'RFLD_EALT',
'SWND_EALT',
'TSUN_EALT',
'TRND_EALT',
'WFIR_EALT',
'VLCN_EALT',
'WNTW_EALT']]

NRI_Map2.rename(columns={'AVLN_EALT': 'Avalanche',
                   'CFLD_EALT': 'Coastal Flooding',
                   'CWAV_EALT': 'Cold Wave',
                   'DRGT_EALT': 'Drought',
                   'ERQK_EALT': 'Earthquake',
                   'HAIL_EALT': 'Hail',
                   'ISTM_EALT': 'Ice Storm',
                   'HWAV_EALT': 'Heat Wave',
                   'HRCN_EALT': 'Hurricane',
                   'LTNG_EALT': 'Lightning',
                   'LNDS_EALT': 'Landslide',
                   'RFLD_EALT': 'Riverine Flooding',
                   'SWND_EALT': 'Strong Wind',
                   'TRND_EALT': 'Tornado',
                   'TSUN_EALT': 'Tsunami',
                   'WFIR_EALT': 'Wildfire',
                   'VLCN_EALT': "Volcanic Activity",
                   'WNTW_EALT': 'Winter Weather',
                    
                    
                  },    inplace=True) 


NRI_Map3=NRI_Map2[['Avalanche',
                   'Coastal Flooding',
                   'Cold Wave',
                   'Drought',
                   'Earthquake',
                   'Hail',
                   'Ice Storm',
                   'Heat Wave',
                   'Hurricane',
                   'Lightning',
                   'Landslide',
                   'Riverine Flooding',
                   'Strong Wind',
                   'Tornado',
                   'Tsunami',
                   'Wildfire',
                   "Volcanic Activity",
                   'Winter Weather']]

NRI_Map3=NRI_Map3.sum()
NRI_Map3=NRI_Map3.to_frame() 
NRI_Map3.reset_index(inplace=True)
NRI_Map3.rename(columns={0: 'Expected Annual Loss'},
          inplace=True)



NRI_Map3=NRI_Map3.sort_values(by=['Expected Annual Loss'], ascending=False)



fig2 = px.bar(NRI_Map3, x='index', y='Expected Annual Loss',
                 labels={"index": "<b> Peril </b>", 'Expected Annual Loss': '<b>Expected Annual Loss ($)</b>' },
                template="simple_white"
            )
fig2.update_traces(marker_color='DarkRed')


#displaying viz 
st.write('**Figure 4: Loss by Peril for**', title_text2)


st.plotly_chart(fig2)

drop_down=NRI_Map3['index']

variable1=st.selectbox(label="Peril to View",
options=(drop_down))

title_text3 = "**" + variable1 + "**"




if State_Name2 == 'CA':
    x2=38.1063
    y2=-120.7367
    zoom=4.5
    
elif State_Name2 == 'FL':
    x2= 28.9331
    y2=-81.87650
    zoom=5
    
elif State_Name2 == 'NY':
    x2= 42.9058
    y2=-75.0933
    zoom=5
    
elif State_Name2 == 'TX':
    x2=31.35394
    y2=-99.25277
    zoom=4

def county_map_2(input_var, map_leg, z):
    fig2 = px.choropleth_mapbox(NRI_Map2, geojson=county, locations='FIPS', color=input_var,
                                   color_continuous_scale="balance",
                                   range_color=map_leg,
                                   mapbox_style="carto-positron",
                                   zoom=z, center = {"lat": x2, "lon": y2},
                                   opacity=0.7,
                                   labels={'STCOFIPS':'FIPS'}
                                  )
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
    st.plotly_chart(fig2)



upper_bound_draft4=NRI_Map2[[variable1]].max()
up4=upper_bound_draft4[0]

pyup4 = up4.item()

pyup5=pyup4


Map_Range3 = st.slider(
    'Edit Map Range',
    0.0, pyup5, pyup5, step = 10000.0)

st.write('**Figure 5: County Level Loss**', title_text3, '**for**', title_text2)

county_map_2(variable1, (0, Map_Range3 ), zoom)

##############################################################################
#section 3
##############################################################################
st.subheader('County Level Correlations with Loss')

st.write("Select States to View in Scatter Plot")



#Enter X variable and Description 
x_value='EAL_VALT'
x_description='<b>Annual Expected Loss by County</b>'

#Enter Y Variable and Description
y_value=st.selectbox(label="Select Variable",
options=('BUILDVALUE', 'POPULATION', 'AGRIVALUE', 'RISK_SCORE', 'SOVI_SCORE' ))


upper_bound_draft5=NRI[[y_value]].max()
up5=upper_bound_draft5[0]

pyup5 = up5.item()


Map_Range4 = st.slider(
    'Edit Map Range',
    0.0, pyup5, pyup5, step = 100000.0)

#data pre-processing 
#defining function 
def scatter_plot(x_value, y_value, y_range):
    fig4 = px.scatter(NRI, x=x_value, y=y_value,
                  #   size="POPULATION",
                     color='STATEABBRV',
                     size_max=15,
                     labels={
                     x_value:x_description,
                    
                 },  template="simple_white")
    fig4.update_layout(transition_duration=500,  xaxis_range=[0, 100000000], yaxis_range=y_range)
    st.plotly_chart(fig4)    


st.write('**Figure 6: Relationship between Expected Loss and Key Variables**')

#running function 
scatter_plot(x_value, y_value, (0, Map_Range4))





