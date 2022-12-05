import json
import re
import time
from fileinput import filename

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

starbucksUrl = "https://www.starbucks.co.kr/store/store_map.do"

driver = webdriver.Chrome()

driver.get(starbucksUrl)

# 화면 최대화
driver.maximize_window()

# 지역 검색 버튼
localSearchXpath = '''//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a'''
driver.find_element_by_xpath(localSearchXpath).click()

# 시도 정보 가져오기
sidoBox = driver.find_element_by_class_name("sido_arae_box")

# 서울을 선택
for sd in sidoBox.find_elements_by_css_selector("li > a"):
    if sd.text.strip() == "서울":   sd.click()

gugunBox = driver.find_element_by_id("mCSB_2_container")


gugunList = gugunBox.find_elements_by_css_selector("ul > li")
for gugun in gugunList:
    if gugun.text.strip() == "전체":
        gugun.click()
time.sleep(2)

req = driver.page_source
soup = BeautifulSoup(req, "html.parser")

content = soup.find(id="mCSB_3_container")

contents = content.find_all("li")

from tqdm import tqdm_notebook

starbucksList = list()
p = re.compile("\s.{1,3}구")
for i in tqdm_notebook(range(len(contents))):
    lat = contents[i]["data-lat"]
    lng = contents[i]["data-long"]
    #     name = contents[i]["data-name"]
    #     code = contents[i]["data-code"]
    #     storecd = contents[i]["data-storecd"]
    # 가게이름
    #     print(contents[i].find("strong").text)
    storeName = contents[i].find("strong").text.strip()
    # 주소
    address = contents[i].find("p", class_="result_details").text.replace("1522-3232", "")
    # 구정보
    gu = p.search(address).group().strip()
    starbucksList.append([storeName, gu, address, lat, lng])

    df_starbucks = pd.DataFrame(starbucksList, columns=["매장이름", "구", "주소", "위도", "경도"])

    ## csv 파일로 데이터 저장.
    df_starbucks.to_csv("서울시 스타벅스.csv", encoding="utf-8-sig", index=False)

    df = pd.read_csv("서울시 스타벅스.csv")
    df
    len(df)
    df.head()

    # 스타벅스를 통해 서울시 구 정보를 guInfo 변수에 저장한다.
    guInfo = df_starbucks["구"].unique()
    print(guInfo)

EDIYAUrl = "https://www.ediya.com/contents/find_store.html#c"

driver = webdriver.Chrome()  # windows .exe
driver.get(EDIYAUrl)

# 주소 검색 버튼 클릭
addressSearchXpath = '''//*[@id="contentWrap"]/div[3]/div/div[1]/ul/li[2]/a'''
driver.find_element_by_xpath(addressSearchXpath).click()

blank = driver.find_element_by_id("keyword_div")

# 검색 입력란
InputBox = blank.find_element_by_css_selector("form > input")
# 검색 버튼 정보
InputButton = blank.find_element_by_css_selector("form > button")

EdiyaList = []
for gu in tqdm_notebook(guInfo):
    InputBox.clear()
    # 주소 입력
    InputBox.send_keys(f"서울 {gu}")
    # 주소 입력이 완료 됐다면 검색 버튼 클릭.
    InputButton.click()
    time.sleep(8)
    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    placeList = soup.find(id="placesList")
    # print("해당 {} 구의 이디야 매장 수 : {}".format(gu, len(placeList.find_all("li", class_="item"))))
    placeLists = placeList.find_all("li", class_="item")
    for j in range(len(placeLists)):
        # 이름
        name = placeLists[j].find("dl").find("dt").text.strip()
        # 주소
        address = placeLists[j].find("dl").find("dd").text.strip()
        EdiyaList.append([name, gu, address])
df_Ediya = pd.DataFrame(EdiyaList,columns=["매장이름","구","주소"])
df_Ediya.head()
## csv 파일로 데이터 저장.
df_Ediya.to_csv("서울시 이디야.csv", encoding="utf-8-sig", index=False)

df_Ediya = pd.read_csv("서울시 이디야.csv")
df_Ediya.head()

df_starbucks.loc[0]
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


# class KakaoLocalAPI:
#
#     def __init__(self, rest_api_key):
#         """
#         Rest API키 초기화 및 기능 별 URL 설정
#         """
#
#         # REST API 키 설정
#         self.rest_api_key = rest_api_key
#         self.headers = {"Authorization": "KakaoAK {}".format(rest_api_key)}
#
#         self.URL_01 = "https://dapi.kakao.com/v2/local/search/address.json"
#         # 02 좌표-행정구역정보 변환
#         self.URL_02 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
#         # 03 좌표-주소 변환
#         self.URL_03 = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
#         # 04 좌표계 변환
#         self.URL_04 = "https://dapi.kakao.com/v2/local/geo/transcoord.json"
#         # 05 키워드 검색
#         self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"
#         # 06 카테고리 검색
#         self.URL_06 = "https://dapi.kakao.com/v2/local/search/category.json"
#
#     def search_address(self, query, analyze_type=None, page=None, size=None):
#         """
#         01 주소 검색
#         """
#         params = {"query": f"{query}"}
#
#         if analyze_type != None:
#             params["analyze_type"] = f"{analyze_type}"
#
#         if page != None:
#             params['page'] = f"{page}"
#
#         if size != None:
#             params['size'] = f"{size}"
#
#         res = requests.get(self.URL_01, headers=self.headers, params=params)
#         document = json.loads(res.text)
#
#         return document
#
#     # rest_api_key = 'Rest API 입력'
#         rest_api_key = '80f054e3171de85c07e45d68682e9003'
#         kakao = KakaoLocalAPI(rest_api_key)
#
#     ## Request
#         result_01 = kakao.search_address(df_starbucks.loc[0]["주소"])
#
#         result_01["documents"][0]["road_address"]["address_name"], result_01["documents"][0]["road_address"]["x"], \
#         result_01["documents"][0]["road_address"]["y"]
#
#     # 잘못 기입한 데이터에 대해서 정제.
#     def processing(x):
#
#         p = re.compile(".*[0-9]+")
#         try:
#             if p.search(x).group() != "":
#                 return True
#             else:
#                 return False
#         except AttributeError:
#             return False
#
#     # 잘못 입력된 이디야 매장 정보 추출.
#     Ediya_errors = df_Ediya[~df_Ediya["주소"].apply(lambda x: processing(x))]
#     Ediya_errors
#
# # 잘못 입력된 정보 인덱스 정보를 변수에 저장한다.
#     errorIndexInfo = Ediya_errors.index
#
#     Url = "https://map.kakao.com/"
#
#     driver = webdriver.Chrome("../driver/chromedriver")  # windows .exe
#     driver.get(Url)
#
#     XPathGo = '''//*[@id="dimmedLayer"]'''
#     XPathGoB = driver.find_element_by_xpath(XPathGo)
#     XPathGoB.click()
#
#     Ediya_errors["주소 지번"] = ""
#
# XPathinput = '''//*[@id="search.keyword.query"]'''
#
# inputaddr = driver.find_element_by_xpath(XPathinput)
# box = driver.find_element_by_class_name("box_searchbar")
#
# for i in range(len(errorIndexInfo)):
#             inputaddr.clear()
#     #time.sleep(1)
#             content1 = df_Ediya.loc[errorIndexInfo[i], "주소"] + " " + df_Ediya.loc[errorIndexInfo[i], "매장이름"] + " 이디야"
#             print("보낼 내용 : ", content1)
#             inputaddr.send_keys(content1)
#             time.sleep(1)
#
#         box.find_element_by_css_selector("button").click()
#         time.sleep(2)
#         req = driver.page_source
#         soup = BeautifulSoup(req, "html.parser")
#         cote = soup.find(id="info.search.place.list")
#         number = cote.find("li", class_="PlaceItem").find("div", class_="info_item").find(class_="lot_number")["title"]
#         print("number : ", number)
#         number = number.split(" ")[-1]
#         Ediya_errors.loc[errorIndexInfo[i], "주소 지번"] = number
# Ediya_errors.head()
# # 원본 데이터와 병합
# df_Ediya = df_Ediya.merge(Ediya_errors[["매장이름","주소 지번"]],on="매장이름",how="outer")
# df_Ediya.head()
# df_Ediya.shape[0] -  df_Ediya[df_Ediya["주소 지번"].isna()].shape[0] == len(errorIndexInfo)
# # nan 값은 모두 빈문자열로 대체
# df_Ediya["주소 지번"].fillna("",inplace=True)
# # 정확한 주소로 수정.
# df_Ediya["주소"] = df_Ediya["주소"] +" "+ df_Ediya["주소 지번"]
# # 해당 컬럼 삭제
# df_Ediya.drop("주소 지번",axis=1,inplace= True)
# df_Ediya
# df = df_Ediya.copy()
# df_Ediya = df.copy()
# df = df_Ediya.copy()
# df_Ediya = df.copy()
#
#
# # 층 이라는 데이터가 주소에 있다면 위도 검색하는데 빈 문자열을 보내기 때문에 해당 표현은 삭제합니다.
# # (성수빌딩) 또는 (한남동) 등 해당 정보 또한 삭제합니다.
# def processing1(x):
#     p = re.compile("\(.*\)")
#     p1 = re.compile("[0-9].[0-9]+층| [0-9]~[0-9]+층|[0-9]+층")
#     text = re.sub(p, '', x).strip()
#     return re.sub(p1, '', text).strip()
#
#
# df_Ediya["주소1"] = df_Ediya["주소"].apply(lambda x: processing1(x))
# df_Ediya.loc[53, "주소1"] = '서울 강북구 도봉로 207'