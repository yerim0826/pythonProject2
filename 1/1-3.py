import json

import pandas as pd
from folium import folium

df_Ediya = pd.read_csv("서울시 이디야(1).csv")
print(df_Ediya.shape)
df_Ediya.head()

df_starbucks.head()
df_starbucks = pd.read_csv("서울시 스타벅스.csv")
print(df_starbucks.shape)
df_starbucks.head()
geo_path = "../data/02. skorea_municipalities_geo_simple.json"
geo_str = json.load(open(geo_path,encoding="utf-8"))

my_map = folium.Map(
    location=[37.5502, 126.982],
    zoom_start=11,
    tiles="Stamen Toner"
)

for idx, rows in df_starbucks.iterrows():
    # location
    lat, lng = rows.위도, rows.경도

    # Marker
    folium.Marker(
        location=[lat, lng],
        popup=rows.매장이름,
        tooltip=rows.주소,
        icon=folium.Icon(
            icon="star",
            color="green",
            icon_color="white",
        )
    ).add_to(my_map)

for idx, rows in df_Ediya.iterrows():
    # location
    lat, lng = rows.위도, rows.경도

    # Marker
    folium.Marker(
        location=[lat, lng],
        popup=rows.매장이름,
        tooltip=rows.주소,
        icon=folium.Icon(
            icon="home",
            color="darkblue",
            icon_color="white",
        )
    ).add_to(my_map)
my_map
