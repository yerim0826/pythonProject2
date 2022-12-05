from selenium import webdriver
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

## 3번
import json
import requests
import folium

# 한글 설정.
import matplotlib.pyplot as plt
import platform
import seaborn as sns
from matplotlib import font_manager, rc

path = "C:/Windows/Fonts/malgun.ttf"

if platform.system() == "Darwin":
    rc("font", family="Arial Unicode MS")
elif platform.system() == "Windows":
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc("font", family=font_name)
else:
    print("Unknown system. sorry")