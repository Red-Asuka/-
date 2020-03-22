import re
import requests
import json
import pandas
from bs4 import BeautifulSoup
from urllib import  request
from datetime import datetime
import os

#获取英雄皮肤壁纸
def getHeroJpg(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    hero_list_img = soup.select('.ui-slide__content > li > img')
    pic_id = 0  # 图片编号
    name = soup.select('.hero-title')[0].text + soup.select('.hero-name')[0].text
    isExists=os.path.exists(name)
    if not isExists:
        os.makedirs(name) 
    for hero_one in hero_list_img:
        hero_img_url = hero_one.get('src')
        print(hero_img_url)
        pic_file = open('./'+name+'/'+name+str(pic_id)+'.jpg', 'wb')  # 二进制创建并写入文件
        pic_file.write(requests.get(hero_img_url).content)  # 写出请求得到的img资源
        pic_id += 1
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
    for url in urls:
        getHeroJpg(urls[url])
    return urls
url = 'http://lol.duowan.com/poppy/'
newsurl = 'http://lol.duowan.com/'
getHeroUrls(newsurl)
