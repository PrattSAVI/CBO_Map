
#%%
import pandas as pd
import folium
import geopandas as gpd

#%% Import Data

gdf = gpd.read_file( r"C:\Users\csucuogl\Desktop\DATA\NYC2017_STEWMAP\NYC2017_STEWMAP_Points_Public_Ext.shp" )


# %%
cols = []
for i in gdf.columns:
    if ('OF_' in i ) or ('Of_' in i ) :
        cols.append(i)

tt = gdf[ ['OrgName'] + cols ].set_index('OrgName')
tt.columns = [ i[3:] for i in tt.columns ]

gdf = gdf[ ['OrgName','OrgWebSite','OrgEmail','geometry','lat','lon'] ]

#%% Undummy
groups = []
for i,r in tt.iterrows():
    tos = r[r==1].index.tolist() 
    text = ','.join( tos ) 
    groups.append( [i,text] )

ttc = pd.DataFrame( data = groups , columns = ['OrgName','Text']).set_index('OrgName')
ttc['Text'] = ttc['Text'].replace( ',' , ', ' , regex = True)
#%% Join the newly created
gdf2 = gdf.join( ttc , on = 'OrgName' )

# %% Create the Map


import numpy as np
gdf2 = gdf2.replace( np.nan , 'Not Available')

map=folium.Map(location=[40.730695 , -73.956338  ],zoom_start=9.5 , tiles = 'cartodbpositron' )

for i,r in gdf2.iterrows():

    popuptext = '<b>Org Name:</b> <br>' + r['OrgName'] + '<br><b>Website:</b><br> <a href=' + r['OrgWebSite'] + '>' +  r['OrgWebSite'] + '</a><br><b>Group Focus:</b> <br>' + r['Text'] + '<br><b>Email: </b><br>' + r['OrgEmail']
    test = folium.Html(popuptext, script=True)
    popup = folium.Popup(test, max_width=450,min_width=200)

    folium.Circle( 
        location = [ r.lon , r.lat ],
        radius = 30,
        fill=True ,
        fillcolor = '#1FB3E5', 
        color = '#1FB3E5',
        tooltip = r['OrgName'],
        popup = popup
        ).add_to(map)

map


# %%

map.save( r'C:\Users\csucuogl\Desktop\WORK\BeyondCovid\Charts\COB_Map\CBO_Map.html' )


# %%
