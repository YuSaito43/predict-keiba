import pandas as pd
import numpy as np
import os
import re
import requests
from bs4 import BeautifulSoup as bs
import time
import gc

#訓練取得
years = ['2016', '2017', '2018', '2019', '2020', '2021']
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
headers = {'User-Agent' : ua}
for year in years:
    url = f"https://sports.yahoo.co.jp/keiba/schedule/yearly?year={year}&type=g1"
    column = ['着順', '枠番', '馬名', '父親', '母親', '性別', '年齢', '体重変化量', '騎手', '人気', '調教師', '種別', '回り方', '距離', '天気', '状態']

    text = requests.get(url, headers=headers)
    text.encoding = text.apparent_encoding
    soup = bs(text.text, "lxml")

    temp = soup.find_all('table')[0].find_all('td')
    urllist = []
    num = 1
    while num < len(temp):
        urllist.append(temp[num].find('a').get('href'))
        num += 6

    res_pd = 0
    flag = 0
    for con in urllist:
        url = "https://sports.yahoo.co.jp" + con
        text = requests.get(url, headers=headers)
        text.encoding = text.apparent_encoding
        ssoup = bs(text.text, "lxml")
    
        types = ssoup.find_all('section', id='racedetail')[0].find_all('span')[1].text.split('・')[0]    #種別
        rotate = ssoup.find_all('section', id='racedetail')[0].find_all('span')[1].text.split('・')[1].split(' ')[0]   #回り方
        length = ssoup.find_all('section', id='racedetail')[0].find_all('span')[1].text.split('・')[1].split(' ')[-1]                 #距離
        weather = ssoup.find_all('section', id='racedetail')[0].find_all('span')[2].text.split('：')[-1]                      #天気
        condition = ssoup.find_all('section', id='racedetail')[0].find_all('span')[3].text.split('：')[-1]                   #状態
        test = ssoup.find('table', class_='hr-table').find_all('tr')
        alllist = []
        for i in range(1, len(test)):
            tlist = []
            temp = test[i].find_all('td')
            if re.sub(r'[\n\t\s]', '', temp[0].text) == '取消':
                continue
            elif re.sub(r'[\n\t\s]', '', temp[0].text) == '中止':
                continue
            elif re.sub(r'[\n\t\s]', '', temp[0].text) == '除外':
                continue
            if '(' in re.sub(r'[\n\t\s]', '', temp[0].text):
                tlist.append(re.sub(r'[\n\t\s]', '', temp[0].text)[:re.sub(r'[\n\t\s]', '', temp[0].text).index('(')])
            else:
                tlist.append(re.sub(r'[\n\t\s]', '', temp[0].text)) #着順
            tlist.append(re.sub(r'[\n\t\s]', '', temp[1].text))     #枠番
            tlist.append(re.sub(r'[\n\t\s]', '', temp[3].find('a').text))   #馬名
            umaURL = 'https://sports.yahoo.co.jp/' + temp[3].find('a').get('href')
            uma_text = requests.get(umaURL, headers=headers)
            uma_text.encoding = uma_text.apparent_encoding
            uma_soup = bs(uma_text.text, "lxml")
            if len(uma_soup.find_all('section', class_='hr-horseProfile')[0].find('div', class_='hr-horsePedigree__gen1st').find_all('div')) == 0:
                tlist.append('-')
                tlist.append('-')
            else:
                parents_list = uma_soup.find_all('section', class_='hr-horseProfile')[0].find('div', class_='hr-horsePedigree__gen1st').find_all('div')
                tlist.append(re.sub(r'[\n\t\s]', '', parents_list[0].text))   #父親
                tlist.append(re.sub(r'[\n\t\s]', '', parents_list[1].text))   #母親
            if re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[0][0] =='せ':
                tlist.append(re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[0][:2])     #性別
                tlist.append(re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[0][2:])     #年齢
            else:
                tlist.append(re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[0][0])   #性別
                tlist.append(re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[0][1:])  #年齢
            tnum = re.sub(r'[\n\t\s]', '', temp[3].find('p').text).split('/')[1]
            tlist.append(tnum[tnum.find('(')+1:tnum.find(')')].strip('+'))                          #体重変化量
            tlist.append(re.sub(r'[\n\t\s]', '', temp[6].find('a').text))                           #騎手
            tlist.append(re.findall(r'\d+', re.sub(r'[\n\t\s]', '', temp[7].text))[0])              #人気
            tlist.append(re.sub(r'[\n\t\s]', '', temp[8].text))                                     #調教師
            tlist.append(types)
            tlist.append(rotate)
            tlist.append(length)
            tlist.append(weather)
            tlist.append(condition)
            alllist.append(tlist)
        res = pd.DataFrame(data=alllist, columns=column)
        if flag == 0:
            res_pd = res
            flag = 1
        else:
            res_pd = res_pd.append(res, ignore_index=True)
        time.sleep(5)
    
    res_pd.to_csv(f'./keiba_result{year}.csv', encoding='utf-8', index=False)

"""#2018年のデータを収集した際に実行
f = pd.read_csv('./keiba_result2018.csv', encoding='utf-8')
f['天気'] = f['天気'].fillna('晴')
f['状態'] = f['状態'].fillna('良')
f.to_csv('./keiba_result2018.csv', encoding='utf-8', index=False)"""