import folium
import requests
import pandas as pd

url_header = 'https://dapi.kakao.com/v2/local/search/address.json?query='
api_key = '80f054e3171de85c07e45d68682e9003'
header = {'Authorization': 'KakaoAK ' + api_key}

def getGeoCoder(address):
    result = ""
    url = url_header + address
    r = requests.get(url, headers=header)
    # print(r)
    if r.status_code == 200:
        try:
            result_address = r.json()["documents"][0]["address"]
            result = result_address["y"], result_address["x"]
        except Exception as err:
            return None
    else:
        result = "ERROR[" + str(r.status_code) + "]"

    return result

def makeMap(매장이름, 구, 주소):
    # 브랜드 이름(brand), 상호명(store), 위도 경도 튜플(geoInfo)
    shopinfo = 구 + 매장이름  # 가게이름(브랜드)
    mycolor = 매장이름
    latitude, longitude = float(geoInfo[0]), float(geoInfo[1])
    # print(longitude, geoInfo[1], shopinfo)

    marker = folium.Marker([latitude, longitude], popup=shopinfo, \
              icon=folium.Icon(color=mycolor, icon='info-sign')).add_to(mapObject)

# 지도의 기준점
# mylatitude = 32.00
mylatitude = 37.56
mylongitude = 126.92
mapObject = folium.Map(location=[mylatitude, mylongitude], zoom_start=13)




csv_flle = '서울시 스타벅스.csv'
myframe = pd.read_csv(csv_flle, index_col=0, encoding='utf-8')

# print(myframe['brand'].unique())
# print(myframe.head())
# print('-' * 40)




mylist = []


import pandas as pd
mapData = pd.mylist

# sido = "제주특별자치도"
# condition1 = myframe['sido'] == sido
# mapData = myframe.loc[condition1]
# print( mapData )
# print('-' * 40)
# mapData = myframe

# mapObject = folium.Map(zoom_start=14)

ok = 0
notok = 0
for idx in range(len(mapData.index)):
    매장이름 = mapData.iloc[idx]['매장이름']
    구 = mapData.iloc[idx]['구']
    주소 = mapData.iloc[idx]['주소']
    geoInfo = getGeoCoder(주소)

    if 주소 == None:
        print('낫오케이 : ' + 주소)
        notok += 1
    else :
        # print(geoInfo)
        print('오케이 : ' + 매장이름 + ' ' + 주소)
        ok += 1
        makeMap(매장이름, 구, 주소)
    print('%'*30)
# end for

# # 지도의 기준점
# mylatitude = 37.56
# mylongitude = 126.92
# folium.Map(location=[mylatitude, mylongitude], zoom_start=14)

total = ok + notok
print('ok :', ok)
print('notok :', notok)
print('total :', total)

filename = 'c:/imsi/caferesult.html'
mapObject.save(filename)

print('파일 저장 완료')