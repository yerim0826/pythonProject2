from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 특정조건을 기다린 뒤 만족하면 넘어가는 기능을 사용하기 위해 사용 (인터넷속도, 사용자이용급증으로 인한 딜레이)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def Get10000labCafeAddress(driver):
    address_list = []
    page = 15
    for i in range(1, page + 1):
        urls = 'https://www.10000lab.com/59/?sort=TIME&keyword_type=all&page='
        final_url = urls + str(i)
        driver.get(final_url)
        map_list = driver.find_elements_by_css_selector('div.map-list-detail > div.map_container')
        for map_item in map_list:
            address = map_item.find_element_by_css_selector('p.adress')
            address_list.append(address.text)

    return address_list

driver = webdriver.Chrome()
Cafe10000labAddressList = Get10000labCafeAddress(driver)
Cafe10000labAddressList
print(Cafe10000labAddressList)


