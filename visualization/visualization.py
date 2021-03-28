# %%
#Creation of datafram dictionnary
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
dico = {}
location = {}
for i in np.arange(1,9):
    dico[i] = pd.read_json(f'visu{i}.json',lines=True)
    location[i] = dico[i]['location'][0]
    dico[i] = dico[i].groupby(by='dateObserved').sum('intensity')
    dico[i].drop(columns=['laneId','reversedLane'], inplace=True)
dico[4]

#%%
# Dataframes don't have the same shape
a={}
for i in np.arange(1,9):
    a[i] = dico[i].shape
a
#%%
#Function which fill missing dates
def fill_date(a):

    dico[a]['Date'] = dico[a].index
    dico[a]

    for i in np.arange(0,dico[a].shape[0]):
        dico[a]['Date'][i] = dico[a].index[i][0:10]

    dico[a]['Date'] = pd.to_datetime(dico[a]['Date'])
    dico[a].index = dico[a]['Date']

    all_days = pd.date_range(dico[a]['Date'].min(), dico[a]['Date'].max(), freq='D')  

    dico[a] = dico[a].reindex(all_days)
    dico[a]['Date'] = dico[a].index
    dico[a] = dico[a].fillna(0)

    for i in np.arange(0,dico[a].shape[0]):
        if (dico[a]['intensity'][i] == 0):
            dico[a]['intensity'][i] = dico[a]['intensity'][i+1]
    return dico[a]

#%%
for i in np.arange(1,9):
    fill_date(i)
#%%
#5th dictionnary needs one more date
dico[5].loc[98] = [557,'2021-03-25']
dico[5]['Date'] = pd.to_datetime(dico[5]['Date'])
dico[5].index = dico[5]['Date']
dico[5]

# %%
#Example of scatter plot of bike traffic at the 2nd location
plt.scatter(dico[2]['Date'],dico[2]['intensity'],color='#ff7f0e')

#%%
#Map with circle markers saved in html format
import folium
pt = []
dict_mtp = {}
for j in np.arange(0,dico[1].shape[0]):
    dict_mtp[j] = folium.Map(location = [43.6162094554924, 3.87440800666809], zoom_start = 12)
    for i in np.arange(1,9):
        pt = list(location[i].values())[0]
        a = pt[0]
        pt[0] = pt[1]
        pt[1] = a
        folium.CircleMarker(radius=dico[i]['intensity'][j]/50, location=pt, color="#3186cc", fill=True, fill_color="#3186cc", popup=f"Intensity:{dico[i]['intensity'][j]} Day:{str(dico[i]['Date'][j])[0:10]}").add_to(dict_mtp[j])
    dict_mtp[j].save(f"mtp_day_{str(dico[i]['Date'][j])[0:10]}.html")
dict_mtp[0]

#%%
#Creating GIF
import imageio
import os

folder = 'pics' 
files = [f"{folder}\\{file}" for file in os.listdir(folder)]

images = [imageio.imread(file) for file in files]
imageio.mimwrite('visualization.gif', images, fps=1)


