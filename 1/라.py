import webbrowser
import folium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def GetPaulBassettAddressList(address):
    driver.get('https://www.baristapaulbassett.co.kr/store/Store.pb')
    shop_list = driver.find_elements_by_css_selector('#shopList > li')
    address_list = []
    for shop in shop_list:
        address = shop.find_element_by_tag_name('address')
        address_list.append(address.text)
    return address_list


driver = webdriver.Chrome()
PaulBassetAddressList = GetPaulBassettAddressList(driver)
PaulBassetAddressList



def Get10000labCafeAddress(driver):
    address_list = []
    page = 15
    for i in range(1, page + 1):
        urls = 'https://www.10000lab.com/59/?sort=TIME&keyword_type=all&page='
        final_url = urls + str(i)
        driver.get(final_url)
        map_list = driver.find_elements_by_css_selector('div.map-list-detail > div.map_container')
        for map_item in map_list:
            address = map_item.find_element_by_css_selector('p.address')
            address_list.append(address.text)

    return address_list




driver = webdriver.Chrome()
Cafe10000labAddressList = Get10000labCafeAddress(driver)
Cafe10000labAddressList

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

for paul in PaulBassetAddressList:
    try:
        Lat, Lng = GetLatLng(paul)
        data = {'Lat': Lat, 'Lng': Lng}
        PaulBassetCoordList.append(data)
    except CoordinationError:
        pass
Cafe10000labCoordList = []

for manlab in Cafe10000labAddressList:
    try:
        Lat, Lng = GetLatLng(manlab)
        data = {'Lat': Lat, 'Lng': Lng}
        Cafe10000labCoordList.append(data)
    except CoordinationError:
        pass





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
    # make_map(PaulBassetCoordList, Cafe10000labCoordList)

    m.save('c:/imsi/cafe.html')

    def auto_open(path):
        cafe = f'{path}'
        make_map.save(cafe)
        new = 2
        webbrowser.open(cafe, new=new)



