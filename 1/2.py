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

starbucksList = []

for starbucks in starbucksList:
    try:
        Lat, Lng = GetLatLng(starbucks)
        data = {'Lat':Lat, 'Lng':Lng}
        starbucksList.append(data)
    except CoordinationError:
        pass
    


