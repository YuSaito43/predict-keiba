import pandas as pd
import numpy as np
import os
import re
import requests
from bs4 import BeautifulSoup as bs
import time
import gc

#レースデータのスクレイピング
column = ['着順', '枠番', '馬名', '父親', '母親', '性別', '年齢', '体重変化量', '騎手', '人気', '調教師', '種別', '回り方', '距離', '天気', '状態']
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
headers = {'User-Agent' : ua}
url = "https://keiba.yahoo.co.jp/race/denma/2205020811/"
text = requests.get(url, headers=headers)
text.encoding = text.apparent_encoding
soup = bs(text.text, "lxml")

types = soup.find('p', id="raceTitMeta").text.split(' | ')[0].split(' ')[0].split('・')[0] #種別
rotate = soup.find('p', id="raceTitMeta").text.split(' | ')[0].split(' ')[0].split('・')[1] #回り方
length = soup.find('p', id="raceTitMeta").text.split(' | ')[0].split(' ')[-1] #距離
weather = soup.find('p', id="raceTitMeta").find_all('img')[0].get('alt') #天気
condition = soup.find('p', id="raceTitMeta").find_all('img')[1].get('alt') #状態

t = soup.find_all('table', class_="mgnBL")[0].find_all('tr')
res_pd = 0
flag = 0
for i in range(1, len(t)):
    m = t[i].find_all('td')
    alllist = []
    alllist.append('-')
    alllist.append(m[1].text) #枠番
    alllist.append(m[2].text.strip('\n').split('\n')[0]) #馬名
    alllist.append(m[5].text.strip('\n').split('\n')[0]) #父親
    alllist.append(m[5].text.strip('\n').split('\n')[1]) #母親
    if m[2].text.strip('\n').split('\n')[1].split(' ')[0][0] == 'せ': #性別
        alllist.append(m[2].text.strip('\n').split('\n')[1].split(' ')[0][:2])
    else:
        alllist.append(m[2].text.strip('\n').split('\n')[1].split(' ')[0][:1])
    alllist.append(re.findall(r'\d', m[2].text.strip('\n').split('\n')[1].split(' ')[0])[0]) #年齢
    alllist.append(m[3].text[m[3].text.find('(')+1:m[3].text.find(')')].strip('+'))                               #体重変化量
    alllist.append(re.sub(r'\d*\.\d', '', m[4].text).replace(' ', '')) #騎手
    alllist.append('-') #人気
    splited = m[2].text.strip('\n').split('\n')[1].split(' ') #調教師
    alllist.append(''.join([splited[1], splited[2][:splited[2].find('(')]]))
    alllist.append(types)
    alllist.append(rotate)
    alllist.append(length)
    alllist.append(weather)
    alllist.append(condition)
    if flag == 0:
        res_pd = pd.DataFrame([alllist], columns=column)
        flag = 1
    else:
        res_pd = res_pd.append(pd.DataFrame([alllist], columns=column), ignore_index=True)
        
res_pd.to_csv('./race_data.csv', index=False, encoding='utf-8')