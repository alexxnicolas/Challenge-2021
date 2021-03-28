#%%
import csv
from download import download
import numpy as np
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
import csv
import seaborn as sns
from ipywidgets import interact

#Download csv
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv'
path_target = "./totem_velo.csv"
download(url, path_target, replace=True)
data = pd.read_csv('totem_velo.csv')
print(data)


# %%
#Rename columns
data.columns = ['Date','Heure','Total cumulé','Total de la journée','Unnamed','Remarque']
data
# %%
#suppression des deux dernières colonnes
data.drop([0,1])
velo = data.drop(columns=['Unnamed','Remarque'])
velo
# %%
velo['Total de la journée'].plot()

# %%
#Convert date into international date
velo_international_date = pd.to_datetime(velo['Date'] + ' ' + velo['Heure'], format='%d/%m/%Y %H:%M:%f')

#%%
#Replacing date in dataframe
velo['Date'] = velo_international_date
velo
# %%
#Drop column hour
velo = velo.drop(columns='Heure')
velo

# %%
#Extract rows with hours between 0:01 am and 9:00 am
import datetime as dt
velo_0_9 = velo[(velo['Date'].dt.hour >= 0) & (velo['Date'].dt.hour <= 8)]
velo_0_9

#%%
#Sum total bike per day
velo_0_9_per_day = velo_0_9.groupby(velo_0_9['Date'].dt.date).sum()
velo_0_9_per_day
# %%
#Drop column 'Total cumulé'
velo_0_9_per_day = velo_0_9_per_day.drop(columns='Total cumulé')
# %%
#Plot of evolution of total bike per day
velo_0_9_per_day.plot()
plt.xlabel('Date')
plt.ylabel('Total bikes')
plt.title("Evolution of total bike per day")
# %%
#Scatter plot of evolution of total bike per day
plt.scatter(velo_0_9_per_day.index, velo_0_9_per_day['Total de la journée'])

# %%
#Outlier
print(velo_0_9_per_day[velo_0_9_per_day['Total de la journée'] == 1191])

velo_0_9_per_day.drop(velo_0_9_per_day[velo_0_9_per_day['Total de la journée'] == 1191].index, inplace=True)
velo_0_9_per_day

# %%
#Creating column with index
velo_0_9_per_day['Date'] = velo_0_9_per_day.index
velo_0_9_per_day
# %%
#Convert column Date in datetime format
velo_0_9_per_day['Date'] = pd.to_datetime(velo_0_9_per_day['Date'])

# %%
#Deleting the first lockdown (march and april)
velo_0_9_per_day.drop(velo_0_9_per_day[(velo_0_9_per_day['Date'].dt.year == 2020) & (velo_0_9_per_day['Date'].dt.month <= 4)].index, inplace=True)

# %%
#Deleting the first lockdown (beginning of may)
velo_0_9_per_day.drop(velo_0_9_per_day[(velo_0_9_per_day['Date'].dt.year == 2020) & (velo_0_9_per_day['Date'].dt.month == 5) & (velo_0_9_per_day['Date'].dt.day <= 10)].index, inplace=True)
velo_0_9_per_day
# %%
#Scatter plot
plt.scatter(velo_0_9_per_day.index, velo_0_9_per_day['Total de la journée'])

#%%
#Index becomes column
velo_0_9_per_day['Date'] = velo_0_9_per_day.index

velo_0_9_per_day = velo_0_9_per_day.rename(columns={'Date':'Jour'})

velo_0_9_per_day['Jour'] = pd.to_datetime(velo_0_9_per_day['Jour'])

velo_0_9_per_day
# %%
#Calculation of median per month
from statistics import median
median_month = velo_0_9_per_day.groupby(by=velo_0_9_per_day['Jour'].dt.month).median()
median_month['Month'] = median_month.index
median_month.reset_index(inplace=True)
median_month.drop(columns='Jour',inplace=True)
median_month['Month'] = median_month['Month'].astype(int)
median_month.loc[11] = ['NaN', 4]
median_month.sort_values(by='Month',inplace=True)
median_month

#%%
#Creation of dictionnary
median_month.index = median_month['Month']
dico = {}
for i in np.arange(1,13):
    dico[i] = median_month['Total de la journée'][i]
    i += 1
dico

#%%
#Converting format
velo_0_9_per_day.index = pd.to_datetime(velo_0_9_per_day.index)
# %%
#Adding missing dates
all_days = pd.date_range(velo_0_9_per_day.index.min(), velo_0_9_per_day.index.max(), freq='D')

velo_0_9_per_day = velo_0_9_per_day.reindex(all_days)

velo_0_9_per_day['Jour'] = velo_0_9_per_day.index

velo_0_9_per_day

#%%
#Reset index
velo_0_9_per_day.reset_index(drop = True,inplace=True)
velo_0_9_per_day

#%%
#Replacing NaN by 0
velo_0_9_per_day.fillna(0,inplace=True)
velo_0_9_per_day
# %%
#Function replacing 0 par median
def replace_median(df):
    for i in np.arange(0,df.shape[0]):
        if (df['Total de la journée'][i] == 0):
            df['Total de la journée'][i] = dico[df['Jour'][i].month]
        i += 1
    return df
replace_median(velo_0_9_per_day)

#%%
#Scatter plot
plt.scatter(velo_0_9_per_day['Jour'], velo_0_9_per_day['Total de la journée'])
# %%
#Linear regression
import scipy as sp
fit = sp.stats.linregress(velo_0_9_per_day.index, velo_0_9_per_day['Total de la journée'])
print(fit)
# %%
#Line equation of regression
fit2 = np.polyfit(velo_0_9_per_day.index, velo_0_9_per_day['Total de la journée'],1)
print(fit2)

# %%
#Polynomial function
poly = np.poly1d(fit2)
# %%
#Prediction of 2nd April
poly(325)

#%%
#Scatter plot of regression
plt.scatter(velo_0_9_per_day.index, velo_0_9_per_day['Total de la journée'])
plt.plot([0.0, 325], [poly(0), poly(325)], 'r-', lw=2)
# %%
