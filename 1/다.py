import requests


# 오류 메시지 처리를 위한 함수 정의
class CoordinationError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# 카카오 지도 rest api를 이용해 위도와 경도 받아오기
def GetLatLng(address):
    result = ''
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    rest_api_key = '80f054e3171de85c07e45d68682e9003'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    r = requests.get(url, headers=header)
    try:
        if r.status_code == 200:
            result_address = r.json()['documents'][0]['address']
            result = result_address['y'], result_address['x']
        else:
            raise CoordinationError('Error')
    except:
        raise CoordinationError('Error')
    return result

PaulBassetCoordList = []

for paul in PaulBassetCoordList:
    try:
        Lat, Lng = GetLatLng(paul)
        data = {'Lat':Lat, 'Lng':Lng}
        PaulBassetCoordList.append(data)
    except CoordinationError:
        pass

Cafe10000labCoordList = []

for manlab in Cafe10000labCoordList:
    try:
        Lat, Lng = GetLatLng(manlab)
        data = {'Lat':Lat, 'Lng':Lng}
        Cafe10000labCoordList.append(data)
    except CoordinationError:
        pass

import folium


def make_map(marker1, marker2):
    m = folium.Map(location=[35.88207, 127.984586], zoom_start=7)
    for i in marker1:
        lat = i['Lat']
        lng = i['Lng']
        folium.Marker(location=[lat, lng],
                      icon=folium.Icon(color='red', icon='Star')).add_to(m)

    for i in marker2:
        lat = i['Lat']
        lng = i['Lng']
        folium.Marker(location=[lat, lng],
                      icon=folium.Icon(color='blue', icon='ok')).add_to(m)

    return m

make_map(PaulBassetCoordList, Cafe10000labCoordList)
make_map(PaulBassetCoordList, Cafe10000labCoordList).save('c:/imsi/paul10000.html')

