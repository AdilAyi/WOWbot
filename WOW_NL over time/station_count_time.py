from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from termcolor import colored
from bs4 import BeautifulSoup
import random
import numpy as np
import pandas as pd
import pickle
import time

import geopandas as gpd
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon

op = webdriver.ChromeOptions()
#op.add_argument('headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
driver.maximize_window()

#go to site
driver.get("https://wow.knmi.nl")

#zoom in to utrecht


time.sleep(10)
driver.quit()