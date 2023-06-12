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

def tableDataText(table):       
    rows = []
    trs = table.find_all('tr')
    for tr in trs[1:]: # for every table row
        rows.append(tr.find_all('td')[0].get_text(strip=True)[-1]) # data row
    return rows

def tableDataText2(table):       
    rows = []
    trs = table.find_all('tr')
    for tr in trs[1:]: # for every table row
        rows.append(tr.find_all('td')[1].get_text(strip=True)) # data row
    return rows

def get_metadata(all_id, random_sec=0, all_id_old=None):
    "station_id now be a batch"
    "Note that all_id and all_id_old must be a list of ids"
    "random_sec makes it possible to let the bot to simulate human behaviour by having random delay in between metadata extraction"
    "A random_sec of 10 makes it that a random amount of seconds in between 0-10 will be taken in between extraction"

    #variable_names as defined in the wow_NL
    variable_names = ['Station ID',
    'Positie',
    'Hoogte (boven zeeniveau)',
    'Tijdzone',
    'Actief station',
    'Data downloaden toegestaan?',
    'Website',
    'Motivatie station',
    'Officieel station',
    'Organisatie', 
    'Ligging',
    'Meting luchttemperatuur',
    'Meting neerslag', 
    'Meting wind', 
    'Stedelijke zone', 
    'Waarneemuren', 
    'lat', 
    'lon',
    'star_rating',
    'description',
    'extra_info']

    #initialize dataset
    df = pd.DataFrame(columns=variable_names)
    ids_error = []

    #NL shape
    NL_shp = gpd.read_file("shapefile/nl_10km.shp")
    NL_shp = NL_shp.to_crs(4326) #change rd to wg84 crs:4326
    
    j=0
    for station_id in all_id:
        if station_id not in all_id_old:
            try:
                #setup driver
                #PATH = "C:\Program Files (x86)\chromedriver.exe"
                #driver = webdriver.Chrome(PATH)
                op = webdriver.ChromeOptions()
                op.add_argument('headless') #so it only happens in the console and the website does not get opened

                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
                driver.maximize_window()

                #go to site
                driver.get("https://wow.knmi.nl/#"+station_id)

                #get coordinates
                time.sleep(1)
                l = driver.find_element(By.XPATH, '//*[@id="myModalLabel"]/span[3]')
                lat, lon = float(l.text.split(',')[0]), float(l.text.split(',')[1])

                point = Point(lon, lat) # longitude, latitude

                # Alternative: if point.within(shape)
                if any(NL_shp.contains(point)):#check if in NL polygon
                    #go to metadata page
                    l2 = driver.find_element(By.XPATH, '//*[@id="modal"]/div[2]/div/div[2]/ul/li[4]')
                    l2.click()

                    #get soup
                    second_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    #TABLE OF GENERAL DATA
                    subset = second_soup.find('div', attrs={'class':'site-details'})
                    table2 = subset.find('table', attrs={'class':'table table-striped'})

                    #TABLE OF METADATA
                    table = second_soup.find('table', attrs={'class':'table table-striped location-attributes'})

                    #STAR RATING
                    star_rating = len(second_soup.find_all('i', attrs={'class':'fa rating fa-star'}))

                    #TEXT
                    beschrijving = second_soup.find('p', attrs={'data-property': 'site.description'}).get_text()
                    extra_info = second_soup.find('p', attrs={'data-property': 'site.additional_information'}).get_text()

                    #extracted data
                    list_table = tableDataText2(table2) + tableDataText(table) + [lat, lon, star_rating, beschrijving, extra_info]
                    #print(colored(list_table, 'red'))
                    #print(colored(variable_names, 'red'))
                    #print(len(list_table) == variable_names)

                    #add to dataset and report progress in prompt
                    print(colored(f"Added station: {station_id}", 'green'))
                    print(colored(f"PROGRESS:  {j+1}/{len(all_id)}",'yellow'))

                    #save dataset to csv
                    df.loc[station_id] = list_table

                    #driver quit to reset the state
                    driver.quit()
                    
                    #every 50 stations save
                    if j%50 == 0:
                        df.to_csv(f"NL_WOW_METADATA.csv")
                    j+=1
                    
                    #random behaviour after extraction if needed
                    if random_sec > 0:
                        time.sleep(random.randint(1, random_sec))
            
            except: 
                with open("ids_error.txt", "w") as f: #save ids with error to a file that assembles all error codes
                    f.write(station_id +"\n")


    #save last df with date and time
    t = time.localtime()
    current_time = time.strftime("%Y%m%d_%Hh%Mm", t)

    df.to_csv(f"data_extracted/NL_WOW_METADATA_{current_time}.csv")
    print(colored("DATA SAVED IN NL_WOW_METADATA.csv", "green"))
    
    return df


#all_id = ['010c7bab-c21f-e911-9462-0003ff5972a6', '81b8a6b0-4110-ed11-b5cf-0003ff5962a8', '44938373-9478-ed11-97b0-0003ff59730c', '12e7004b-1926-ed11-b5cf-0003ff59a71f', '6da1db89-2b5e-ea11-b698-0003ff599880', '9ffd043e-4a57-e711-9400-0003ff596cbf', '924726001']
all_id = np.loadtxt('station_ids.txt', dtype='str').tolist()
get_metadata(all_id) #execute

