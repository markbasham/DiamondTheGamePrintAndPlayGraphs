import geopandas as gpd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
from matplotlib.ticker import ScalarFormatter
import matplotlib.colors as colors

# set the filepath and load in a shapefile
fp = 'geoassets/england_pca_2012.shp'
england_df = gpd.read_file(fp)
# check data type so we can see that this is not a normal dataframe, but a GEOdataframe

fp = 'geoassets/wales_pca_2012.shp'
wales_df = gpd.read_file(fp)

fp = 'geoassets/scotland_pca_2012.shp'
scotland_df = gpd.read_file(fp)

print(england_df)
print(scotland_df)
print(wales_df)

all_df = england_df.append(scotland_df).append(wales_df)

print(all_df)

# Now the map is sorted out, add the data
import pandas as pd
import numpy as np
df = pd.read_csv("data/Questionaire_Responces.csv")
del df['UserID']
del df['UserNo']
del df['Started']
del df['Ended']
del df['Q1']
del df['Q4']
del df['Q5']
del df['Q6']
df['Q3.1'] = df['Q3.1. 0 - 7 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.2'] = df['Q3.2. 8 - 14 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.3'] = df['Q3.3. 15 - 19 years old'].replace('-','0').replace(np.NaN,0).astype(int)
df['Q3.4'] = df['Q3.4. 20 +'].replace('-','0').replace(np.NaN,0).astype(int)
df['total'] = df['Q3.1']+df['Q3.2']+df['Q3.3']+df['Q3.4']
df = df[df['UK'] == 1.0]
df['label'] = df['Q2'].str.split('[0-9]').str[0].str.upper()

# pull out individuals only
df_ind = df[df['total']<=10]
df_big = df[df['total']>10]

df_ind = df_ind.groupby('label').agg({'Q3.1':['sum'],'Q3.2':['sum'],'Q3.3':['sum'],'Q3.4':['sum'],'total':['sum']})
df_big = df_big.groupby('label').agg({'Q3.1':['sum'],'Q3.2':['sum'],'Q3.3':['sum'],'Q3.4':['sum'],'total':['sum']})
df_ind.columns = df_ind.columns.get_level_values(0)
df_big.columns = df_big.columns.get_level_values(0)

print(df_ind)

#merge the 2 datasets, for institutanal and individual
df_ind = pd.merge(all_df, df_ind, on=['label'], how='left')
df_big = pd.merge(all_df, df_big, on=['label'], how='left')

# create figure and axes for Matplotlib
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8), dpi=300)

# create map
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
fig.suptitle('Boardgame players in Britain', fontsize=16)
ax1.set_title('Small Groups', \
              fontdict={'fontsize': '14'})
ax2.set_title('Large Goups', \
              fontdict={'fontsize': '14'})

# Create colorbar as a legend
formatter = ScalarFormatter()
sm1 = plt.cm.ScalarMappable(cmap='viridis_r',
                            norm=colors.LogNorm(vmin=df_ind['total'].min(),
                                                vmax=df_ind['total'].max()),
                            )
sm1._A = []
cbar1 = fig.colorbar(sm1, ax=ax1, shrink=0.4, format=formatter, ticks=[1,2,5,10,20,50,100,200,500,1000,2000])

sm2 = plt.cm.ScalarMappable(cmap='viridis_r',
                            norm=colors.LogNorm(vmin=df_big['total'].min(),
                                                vmax=df_big['total'].max())
                            )
sm2._A = []
cbar2 = fig.colorbar(sm2, ax=ax2, shrink=0.4, format=formatter, ticks=[1,2,5,10,20,50,100,200,500,1000,2000])


# this will save the figure as a high-res png. you can also save as svg
fig.savefig('figures/PlayersInBritain.png', dpi=300)