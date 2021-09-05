from libs import browser_init, insta_login
import pandas as pd 
import numpy as np
import os 
import sys
from datetime import datetime
from pathlib import Path

#initialising the connection
browser = browser_init()
insta_login(browser)

# Setting up a dict with the name and insta accounts of profiles to scrape
dct={}
dir = Path(__name__).resolve().parents[1]
dir= str(dir)+'/data_repo/Comp_insta.xlsx'

def load_data(dir):
    sheet = pd.read_excel(dir,engine='openpyxl')
    return sheet

sheet = load_data(dir)

for index in range(sheet.shape[0]):
    name=sheet.iloc[index,0]
    page=sheet.iloc[index,1]
    dct[name]=page
    print(sheet.iloc[index,0],sheet.iloc[index,1])

# Requesting the data
data = {}
for name, page in dct.items():
    print(f'Getting page: {page}')
    try:
        browser.get(page)
        data[name]={}
        data[name]['date']= datetime.now()
        for elem in browser.find_elements_by_xpath('//li[@class = "Y8-fY "]'):
            print(f'elem.text: {elem.text}')
            try:
                elem = elem.text.split(' ')
                data[name][elem[1]]=elem[0]
                print(f'appended: {data[name][elem[1]]}')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        pass

# Dataframe to structure this run's data pull
df1 = pd.DataFrame.from_dict(data,orient='index',columns=['date','posts','followers','following'])

# Writing to csv
path = Path(__name__).resolve().parents[1]

if 'demo.csv' not in os.listdir(str(path)+'/data_repo'):
    df1.to_csv(str(path)+'/data_repo/demo.csv', header= True)
else:
    df1.to_csv(str(path)+'/data_repo/demo.csv', header= False, mode= 'a')