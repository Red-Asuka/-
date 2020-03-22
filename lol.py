import re
import requests
import json
import pandas
from bs4 import BeautifulSoup
from datetime import datetime

#利用多玩获取所有英雄首页
def getHeroUrls(newsurl):
    urls = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    res = soup.select('#champion_list > li > a')
    for i in res:
        url = i['href']
        name = i.text
        urls[name] = url
#    print(urls)
    return urls
#获取单个英雄信息
def getHeroInfo(url):
    Hero = {}
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    Hero['姓名'] = soup.select('.hero-title')[0].text + soup.select('.hero-name')[0].text
    Hero['背景故事'] = soup.select('.hero-popup__txt')[0].text
#    Hero['位置'] = soup.select('.hero-tag')[0].text + ' ' + soup.select('.hero-tag')[1].text
    li = soup.select('.hero-box__bd > ul > li')
    for i in li:
        #沙雕程序员不用放什么空标签[○･｀Д´･ ○]
        if(i.select('em') != []):
            Hero[i.select('em')[0].text] = i.select('span')[0].text
    print(Hero)
    return Hero
#批量获取
def getHerosInfo(urls):
    result = []
    for url in urls:
#        rse = getHeroInfo(urls[url])
#        print(rse)
        result.append(getHeroInfo(urls[url]))
    return result
newsurl = 'http://lol.duowan.com/'
result = {}
date = getHerosInfo(getHeroUrls(newsurl))
df = pandas.DataFrame(date)
df.to_excel('hero.xlsx')