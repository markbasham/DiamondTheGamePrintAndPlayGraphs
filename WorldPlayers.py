import geopandas as gpd
import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.ticker import LogFormatter
from matplotlib.ticker import ScalarFormatter
import matplotlib.colors as colors

# set the filepath and load in a shapefile
fp = 'geoassets/ne_50m_admin_0_countries.shp'
all_df = gpd.read_file(fp)

all_df = all_df[all_df['NAME'] != 'Antarctica']

# Now the map is sorted out, add the data
import pandas as pd
import numpy as np
df = pd.read_csv("data/Questionaire_Responces.csv")
del df['UserID']
del df['UserNo']
del df['Ended']
del df['Q1']
del df['Q4']
del df['Q5']
del df['Q6']
df['Started'] = pd.to_datetime(df['Started'])
df = df.set_index(['Started'])
df['Q3.1'] = df['Q3.1. 0 - 7 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.2'] = df['Q3.2. 8 - 14 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.3'] = df['Q3.3. 15 - 19 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.4'] = df['Q3.4. 20 +'].replace('-','0').replace(np.NaN,0).astype(int)
df['total'] = df['Q3.1']+df['Q3.2']+df['Q3.3']+df['Q3.4']
df['Q2'][df['UK']==1.0] = 'United Kingdom'
df['NAME'] = df['Q2']

clean_df = df.copy()

start_date = '2020-6-1'
end_date = '2022-06-9'
# set the range, start date set before to pick up any early ones where plotting is problematic
df = clean_df.loc[start_date:end_date]

# seperate personal and institutional data
df_ind = df[df['total']<=10]
df_big = df[df['total']>10]

# aggregate the data by postcode region
df_ind = df_ind.groupby('NAME').agg({'Q3.1':['sum'],'Q3.2':['sum'],'Q3.3':['sum'],'Q3.4':['sum'],'total':['sum']})
df_big = df_big.groupby('NAME').agg({'Q3.1':['sum'],'Q3.2':['sum'],'Q3.3':['sum'],'Q3.4':['sum'],'total':['sum']})
df_ind.columns = df_ind.columns.get_level_values(0)
df_big.columns = df_big.columns.get_level_values(0)

#merge the 2 datasets with map data
df_ind = pd.merge(all_df, df_ind, on=['NAME'], how='left')
df_big = pd.merge(all_df, df_big, on=['NAME'], how='left')

# create figure and axes for Matplotlib
fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), dpi=300)

# create maps
plt1 = df_ind.plot(cmap='viridis_r',
                   linewidth=0.5,
                   ax=ax1,
                   edgecolor='0.0',
                   column=('total'),
                   missing_kwds={"color": "lightgrey",
                                 "edgecolor": "black",
                                 "label": "Missing values",
                                 },
                   norm=colors.LogNorm(vmin=df_ind['total'].min(),
                                       vmax=df_ind['total'].max()),
                   )
plt2 = df_big.plot(cmap='viridis_r',
                   linewidth=0.5,
                   ax=ax2,
                   edgecolor='0.0',
                   column=('total'),
                   missing_kwds={"color": "lightgrey",
                                 "edgecolor": "black",
                                 "label": "Missing values",
                                 },
                   norm=colors.LogNorm(vmin=df_big['total'].min(),
                                       vmax=df_big['total'].max()),
                   )

# Now we can customise and add annotations

# remove the axis
ax1.axis('off')
ax2.axis('off')

# add a title
fig.suptitle(f'Boardgame players Globally\nfrom {start_date} to {end_date}', fontsize=16)
ax1.set_title('Personal', \
              fontdict={'fontsize': '14'})
ax2.set_title('Institutional', \
              fontdict={'fontsize': '14'})

# Create colorbar as a legend
formatter = ScalarFormatter()
sm1 = plt.cm.ScalarMappable(cmap='viridis_r',
                            norm=colors.LogNorm(vmin=df_ind['total'].min(),
                                                vmax=df_ind['total'].max()),
                            )
sm1._A = []
cbar1 = fig.colorbar(sm1, ax=ax1, shrink=0.7, format=formatter, ticks=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000])

sm2 = plt.cm.ScalarMappable(cmap='viridis_r',
                            norm=colors.LogNorm(vmin=df_big['total'].min(),
                                                vmax=df_big['total'].max())
                            )
sm2._A = []
cbar2 = fig.colorbar(sm2, ax=ax2, shrink=0.7, format=formatter, ticks=[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000])


# this will save the figure as a high-res png. you can also save as svg
fig.savefig('figures/WorldPlayers.png', dpi=300)

# get back to the original datasets for plotting dat a over time
# seperate personal and institutional data
df_ind = df[df['total']<=10]
df_big = df[df['total']>10]

# for the individual data, make a plot of total vrs time
plt.rcParams["figure.dpi"] = 300
plt.clf()
plt.cla()
title = "Personal players over time globally"
df_ind_sum = df_ind['total'].sort_index().cumsum()
ax = df_ind_sum.plot(kind='line', x='date', rot=90, stacked=True, colormap=pl.cm.viridis, figsize=(8, 6), title=title)
ax.set_ylabel("Number of People")
fig = ax.get_figure()
fig.tight_layout()
fig.savefig('figures/TotalWorldPlayersOverTime.png', dpi=300)

# for the group data, make a plot of total vrs time
plt.rcParams["figure.dpi"] = 300
plt.clf()
plt.cla()
title = "Institutional players over time globally"
ax = df_big['total'].sort_index().cumsum().plot(kind='line', x='date', rot=90, stacked=True, colormap=pl.cm.viridis, figsize=(8, 6), title=title)
ax.set_ylabel("Number of People")
fig = ax.get_figure()
fig.tight_layout()
fig.savefig('figures/TotalWorldGroupsOverTime.png', dpi=300)