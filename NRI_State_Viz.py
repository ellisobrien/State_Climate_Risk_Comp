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
st.title("Evaluating Natural Disaster and Climate Risk in California, Florida, New York, and Texas")

#Adding text describing issue 
st.write('Natural disasters present a fundamental risk to housing and economic security in the U.S. In 2021 alone natural disasters cost the U.S $145 Billion. In an effort to improve data surrounding natural disasters, the Federal Emergency Management Agency released the National Risk Index (NRI) which provides comprehensive county level data on natural disaster risks.')

st.write('This dashboard uses NRI data to analyze and visualize climate risk in four states: California, Florida, New York and Texas. These states represent the four most populous states in the country and the four states with over 2 trillion dollars in building value. Additionally, California, Texas, and Florida represent the three states with the highest expected annual loss due to climate change. Analyzing these states allows us to see the risk profile of four distinct regions in the country.')

st.write('This tool is intended for federal, state, and local policy makers, who may use it to gain a better understanding of geospatial risk in their state. However, it can be used by anyone, for example a perspective property buyer seeking to understand the climate risk associated with their future properties.')


#imporing json 
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    county = json.load(response)
    
#importing data from github
NRI=pd.read_csv('https://raw.githubusercontent.com/ellisobrien/State_Climate_Risk_Comp/main/NRI_State_Dat.csv', dtype={"STCOFIPS": str})

#renaming county fips code
NRI.rename(columns={'STCOFIPS':'FIPS'}, inplace=True)




##############################################################################
#section 1
##############################################################################
#section header
st.header('Overview of Loss by State and County Risk')

#section desrciption
st.write("This section provides a high level understanding of loss and risk for each state analyzed.")



#selecting key states for scatter plot
nri_plot_1=NRI[['STATEABBRV', 'EAL_VALB', "EAL_VALA", "EAL_VALPE"]]

#summinng features
nri_plot_1=nri_plot_1.groupby('STATEABBRV').sum()

#making state a coumumn
nri_plot_1.reset_index(inplace=True)

#sorting data for plot
nri_plot_1=nri_plot_1.sort_values(by=['EAL_VALB'], ascending=False)

#renaming columns
nri_plot_1.rename(columns={'EAL_VALB': 'Building Loss',
                         'EAL_VALA': 'Agricultural Loss',
                         'EAL_VALPE': 'Population Loss'},
                                           inplace=True)

#making bar graph
fig0 = px.bar(nri_plot_1, x="STATEABBRV", 
             y=['Building Loss', 'Agricultural Loss', 'Population Loss'], 
             labels={"value": "Annual Estimated Loss ($)", 'STATEABBRV':'State', "variable": "Loss Breakdown"},
             color_discrete_map={"Building Loss": "silver", "Agricultural Loss": "green", 'Population Loss':'black'},
             template="simple_white",
             height=400)
fig0.update_layout(title_text = '<b>Figure 1: State Level Loss Broken Down by Loss Type </b> <br><sup> California and Texas Lead All States in Loss </sup>')

#displaying viz
st.plotly_chart(fig0)

#adding cpation
st.caption('Buildings are the primary driver of loss from natural disasters. While agricultural loss is not as financially damaging, food systems could be strained as climate change intensifies. In this dataset population is defined as the injury or loss of life from natural disasters converted to dollar terms. It is interesting that California leads in building and agricultural loss, but Texas has the largest population loss by a significant margin.')

#adding space
st.text("")

st.text("")

st.text("")

st.text("")

#Adding header
st.subheader('Maps of Loss and Risk')

#Providng context
st.write('Select a state from the drop down below to view county level loss and risk maps for the state you select.') 
 
#initiating dropdown
State_Name1=st.selectbox(label="Select State to View",
options=('CA', 'FL', 'NY', 'TX' ))

#writing text
st.write('Figure 2 shows annual expected loss by county for the state you select. Figure 3 shows the composite risk score (composite risk score is described below figure 3). Hover your cursor over a county on the map to see the specific loss/risk for that county. Hover information in figure 2 also shows vulnerability and reslience ratings as provided by FEMA. Descriptions and definitions of loss, risk, vulnerability, and reslience can be accessed from this webpage: https://hazards.fema.gov/nri/')
title_text = "**" + State_Name1 + "**"

#spacing
st.text("")

st.text("")


#setting zoom and map range based on state name 
if State_Name1 == 'CA':
    x=38.1063
    y=-120.7367
    Map_Range2=(0,500000000)
    zoom=4.5
    
elif State_Name1 == 'FL':
    x= 27.36895
    y=-82.30029
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
    zoom=4.5


#filtering based on state name
NRI_MAP1=NRI[NRI.STATEABBRV == State_Name1]


#initilizing mapping function 
def county_map_1(input_var, map_leg, z, input_desc):
    fig1 = px.choropleth_mapbox(NRI_MAP1, geojson=county, locations='FIPS', color=input_var,
                                   color_continuous_scale="balance",
                                   range_color=map_leg,
                                   mapbox_style="carto-positron",
                                   zoom=z, center = {"lat": x, "lon": y},
                                   opacity=0.7,
                                   hover_name="COUNTY", hover_data=["SOVI_RATNG", "RESL_RATNG"],
                                   labels={input_var: input_desc, 'STCOFIPS':'FIPS', 'SOVI_RATNG':'Social Vulnerability', 'RESL_RATNG':'Resilience'}
                                  )
    fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
    st.plotly_chart(fig1)


#writing map title 
st.write('**Figure 2: Annual Expected Loss by County for**', title_text)
st.caption('Highly Populated Coastal Areas Tend to Have the Highest Expected Losses')


#Enter Variables to Map here 
variable_to_map_NRI2='EAL_VALT'

#Enter Variable Description 
NRI_description2='Annual Expected Loss'

#running function 
county_map_1(variable_to_map_NRI2, Map_Range2, zoom, NRI_description2)

#writing caption
st.caption('Losses are heavily influenced by two factors: peril frequency/intensity and population. Population is highly correlated with loss since there tends to be more infrastructure and exposure in highly populated areas. For example, while Miami-Dade County and Los Angeles County are not inherently higher risk than their neighboring counties, their losses are much higher due to population.')

st.caption('_Please note that the loss range changes for each state in the above figure so that higher and lower loss counties can be differentiated between within a state._')

#spacing format
st.text("")

st.text("")

st.text("")

#title and caption for figure 3
st.write('**Figure 3: Composite Risk Score by County for**', title_text)
st.caption('_Risk Score Takes Into Account Composite Risk From All Perils_')

#Enter Variables to Map here 
variable_to_map_NRI1='RISK_SCORE'

#Enter Variable Description 
NRI_description1='Composite Risk Score'

#setting map range 
Map_Range1=(0,50)
#running mapping function
county_map_1(variable_to_map_NRI1, Map_Range1, zoom, NRI_description1)

st.caption('Risk Score takes into account risk from all 18 Perils in the risk index, as well as social vulnerability and community relience. While it is still highly correlated with expected loss in this map we start to see more rural, less populated areas with higher risk scores relative to their expected loss.')


#writing map title 2

##############################################################################
#section 2
##############################################################################

#spacing
st.text("")

st.text("")

st.text("")

#writing section hearder
st.header('Analysis of Peril-Specific Loss by State ')
st.write('Section one was intended to provide a high level overview of climate risk. This section identifies the primary perils for each state.')

#spacing 
st.text("")

st.text("")


#dropdown directions
st.write('Select a state from the dropdown below to see which perils drive losses in the state.')

#setting drop down menu
State_Name2=st.selectbox(label="Select State",
options=('CA', 'FL', 'NY', 'TX' ))

#formatting state name for title
title_text2 = "**" + State_Name2 + "**"

#filtering text based on state name
NRI_Map2=NRI[NRI.STATEABBRV == State_Name2]

#filling NA
NRI_Map2 = NRI_Map2.fillna(0)

#selecting columns for map
NRI_Map2=NRI_Map2[['FIPS', 'COUNTY', 'AVLN_EALT',
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

#renaming columns 
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

#setting new map
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

#summing values
NRI_Map3=NRI_Map3.sum()
#converting to data frame
NRI_Map3=NRI_Map3.to_frame() 
#renaming columns 
NRI_Map3.reset_index(inplace=True)
NRI_Map3.rename(columns={0: 'Expected Annual Loss'},
          inplace=True)


#SORTING for bar graph
NRI_Map3=NRI_Map3.sort_values(by=['Expected Annual Loss'], ascending=False)


#making bargraph
fig2 = px.bar(NRI_Map3, x='index', y='Expected Annual Loss',
                 labels={"index": "<b> Peril </b>", 'Expected Annual Loss': '<b>Expected Annual Loss ($)</b>' },
                template="simple_white"
            )
fig2.update_layout(title_text = '<b>Figure 4: Loss by Peril For Selected State </b> <br><sup> Risk Profiles are Very Different Across States </sup>')
fig2.update_traces(marker_color='DarkRed')

#displaying bargraph
st.plotly_chart(fig2)
#displaying caption
st.caption('Earthquake is the leading cause of loss in California, inland flooding is the leading cause of loss in New York, hurricane is the leading cause of loss in Texas and Florida. Different regions, climates, and geographies contrinbute to very different dominant perils across states.')

#spacing
st.text("")

st.text("")

st.text("")

st.text("")

st.text("")
#Section subheader
st.subheader('Map of Peril Specific Losses')
#directions
st.write('Select a peril from the dropdown below to see the perils county level losses for your selected state. You can also adjust the slider below to alter the map range to see more or less differentiation betwen counties.')

#map dropdown
variable1=st.selectbox(label="Peril to View",
options=('Coastal Flooding',
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
                   'Wildfire',
                   'Winter Weather'))

#formatting title text 
title_text3 = "**" + variable1 + "**"



#setting zoom and postion based on state selection
if State_Name2 == 'CA':
    x2=38.1063
    y2=-120.7367
    zoom=4.5
    
elif State_Name2 == 'FL':
    x2= 27.36895
    y2=-82.30029
    zoom=5


elif State_Name2 == 'NY':
    x2= 42.9058
    y2=-75.0933
    zoom=5
    
elif State_Name2 == 'TX':
    x2=31.35394
    y2=-99.25277
    zoom=4.5

#defining mapping function
def county_map_2(input_var, map_leg, z):
    fig3 = px.choropleth_mapbox(NRI_Map2, geojson=county, locations='FIPS', color=input_var,
                                   color_continuous_scale="balance",
                                   range_color=map_leg,
                                   mapbox_style="carto-positron",
                                   zoom=z, center = {"lat": x2, "lon": y2},
                                   opacity=0.7,
                                   hover_name="COUNTY",
                                   labels={'STCOFIPS':'FIPS'}
                                  )
    fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='usa')
    #showing fiugre 
    st.plotly_chart(fig3)


#set
upper_bound_draft4=NRI_Map2[[variable1]].max()
up4=upper_bound_draft4[0]
pyup4 = up4.item()


#setting 
Map_Range3 = st.slider(
    'Edit Map Range (Map range values are in Dollars)',
    0.0, pyup4, pyup4*.5, step = 10000.0)

st.write('**Figure 5: County Level**', title_text3, '**Expected Loss for**', title_text2)
st.caption('Geographic Region Determine Peril Vulnerability by State')

county_map_2(variable1, (0, Map_Range3 ), zoom)
st.caption('Most states are only threatened by a few perils with virtually no risk from other types of disasters. For example, while California has the highest annual expected loss in the country it has virtually no hurricane risk due to cold waters in the Pacific Ocean.')


st.text("")

st.text("")

st.text("")

##############################################################################
#section 3
##############################################################################
st.header('County Level Correlations with Loss')

st.write("This section provides an overview of the correlations between expected loss and key exposure and risk metrics. Exposure (i.e., building value, population) and risk (i.e., risk score and social vulnerability) dictate losses so it is useful to see corelations between loss and each of these factors. Each point on the below charts represents a county. It is perhaps less useful to examine low loss counties on these graphs but they are useful for indentifying high risk/high loss outliers.")

st.text("")

st.text("")

st.text("")

NRI_Scatter=NRI[['COUNTY','STATEABBRV', 'BUILDVALUE', 'POPULATION', 'AGRIVALUE', 'RISK_SCORE', 'SOVI_SCORE', 'RESL_SCORE', 'EAL_VALT']]

NRI_Scatter.rename(columns={'STATEABBRV': 'State',
                    'BUILDVALUE': 'Building Value ($)',
                   'POPULATION': 'Population',
                   'AGRIVALUE': 'Agricultural Value ($)',
                   'RISK_SCORE': 'Risk Score',
                   'SOVI_SCORE': 'Social Vulnerability',
                   'RESL_SCORE': 'Community Resilience',
                   'EAL_VALT': 'Expected Annual Loss'
                  },    inplace=True) 


#Enter X variable and Description 
x_value='Expected Annual Loss'
x_description='Annual Expected Loss by County ($)'

#settingsection 
st.write('**Examining Relationship Between Loss and Exposure**')
st.write('Select an exposure metric from the drop down below to see how it is correlated with loss. Additionally, you can adjust the slider to alter the y or x axis. The slider slides from the minimum and maximum possible value for each axis.')
#Enter Y Variable and Description
y_value=st.selectbox(label="Select Variable",
options=("Building Value ($)",
'Population',
'Agricultural Value ($)'))


#converting values to floats
NRI_Scatter["Population"] = NRI_Scatter["Population"].astype(float)
NRI_Scatter["Agricultural Value ($)"] = NRI_Scatter["Agricultural Value ($)"].astype(float)

#setting slider range
upper_bound_draft5=NRI_Scatter[[y_value]].max()
up5=upper_bound_draft5[0]
pyup5 = up5.item()

#inputting slideer
Map_Range4 = st.slider(
    'Edit Y-Axis',
    0.0, pyup5, pyup5*.5, step = 100000.0)

#setting slider range
upper_bound_draft6=NRI_Scatter[[x_value]].max()
up6=upper_bound_draft6[0]
pyup6 = up6.item()

#implementing slider
Map_Range5 = st.slider(
    'Edit X-Axis, Expected Loss',
    0.0, pyup6, pyup6*.2, step = 100000.0)


#defining function 
def scatter_plot(x_value, y_value, y_range, x_range):
    fig4 = px.scatter(NRI_Scatter, x=x_value, y=y_value,
                     color='State',
                     size_max=15,
                     hover_name="COUNTY",
                     labels={
                     x_value:x_description,
                    
                 },  template="simple_white")
    fig4.update_layout(title_text = '<b>Figure 6: Relationship between Expected Loss and Exposure </b> <br><sup> All Types of Exposure are Highly Correlated with Loss </sup>', transition_duration=500,  xaxis_range=x_range, yaxis_range=y_range)
    st.plotly_chart(fig4)    



#running function 
scatter_plot(x_value, y_value, (0, Map_Range4), (0, Map_Range5))

#data caption 
st.caption('Building Value and Population tend to be highly correlated with loss. But this pattern is not as strong across all states. In New York for example, there are many high loss high population counties that have low relative loss.')
#text spacing 
st.text("")

st.text("")

st.text("")

#setting subheading
st.write('**Examining Relationship Between Loss and Risk Metrics**')
st.write('')
#select box for dropdown 2
y_value2=st.selectbox(label="Select Risk Variable",
options=('Risk Score',
'Social Vulnerability',
'Community Resilience'))


#setting x value
x_value2='Expected Annual Loss'

#setting slider range 
upper_bound_draft7=NRI_Scatter[[x_value2]].max()
up7=upper_bound_draft7[0]

pyup7 = up7.item()

#inputting slider 
Map_Range6 = st.slider(
    'Edit X-Axis, Expected Loss',
    0.0, pyup7, pyup7*.2, step = 100000.00, key=9)



#defining function 
def scatter_plot2(x_value, y_value, map_range):
    fig5 = px.scatter(NRI_Scatter, x=x_value, y=y_value,
                     color='State',
                     size_max=15,
                     hover_name="COUNTY",
                     labels={
                     x_value:x_description,
                    
                 },  template="simple_white")
    fig5.update_layout(title_text = '<b>Figure 7: Relationship between Expected Loss and Exposure </b> <br><sup> Risk and Loss are Highly Correlated </sup>', transition_duration=500,  xaxis_range=map_range)
    st.plotly_chart(fig5)

#running function
scatter_plot2(x_value2, y_value2, (0, Map_Range6))

#writing caption
st.caption('According to FEMA, risk score and social vulnerability should be highly correlated with loss, while community resilience should be negativley correlated with loss. This chart shows a strong positive correlation between risk and loss, but the relationship between vulnerability and resilience is weaker.')


#Adding in authors contact 
st.markdown('_For questions and support contact Ellis Obrien: eso18@georgetown.edu_')



