#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#File    :   downtxt.py
#Time    :   2021/07/08 15:19:27
#Author  :   drov 
#Version :   1.3
#Contact :   drov.liu@gmail.com
#Desc    :   None
#usage   :   usage: downtxt.py [-h] [-v] [-n NAME]
#

from hashlib import new
import os,sys,time
import argparse
from urllib import response
from urllib.parse import quote,urlencode
from urllib.request import urlopen
from bs4 import BeautifulSoup as bf
import requests
import rarfile
import tempfile

local_path = os.path.dirname(os.path.realpath(__file__))
logger = open(local_path+'/log.txt','a+')

def download(_down_url,_book_name):
    global local_path
    re_code = 'none'
    data = ''
    for url in _down_url:
        response = requests.get(url)
        con_type = response.headers['Content-Type']
        if response.status_code == 200:
            re_code='done'
            data = response.content
            break
    if data == '':
        return 'none'
    if 'rar' in con_type:
        _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
        _tmp_file.write(data)  # byte字节数据写入临时文件
        rar = rarfile.RarFile(_tmp_file)
        rar.extractall(local_path+'/txt')
        _tmp_file.close()
        return re_code
    elif 'text/plain' in con_type:
        f = open(local_path+'/txt/'+_book_name+'.txt','wb+')
        f.write(data)
        f.close()
        return re_code
    return 'type err'

def down_zxcs(_url):
    print(_url)
    html = urlopen(_url)
    obj = bf(html.read(),'html.parser')
    book_name = obj.h2.get_text()
    down_url = []
    for tag in obj.find_all("span", class_="downfile"):
        down_url.append(tag.a.get('href'))
    return book_name,down_url

def down_ksw(_url):
    html = urlopen(_url)
    obj = bf(html.read(),'html.parser')
    book_name = obj.h1.get_text()
    down_url = []
    for tag in obj.find_all("li"):
        if tag.a.get_text() == 'TXT下载':
            down_url.append(tag.a.get('href'))
    return book_name,down_url

def down_ijjxsw(_url):
    html = urlopen(_url)
    obj = bf(html.read(),'html.parser')
    book_name = obj.h1.get_text()
    down_url = []
    for tag in obj.find_all("li"):
        if tag.a and tag.a.get_text() == '下载TXT电子书':
            html = urlopen('https://m.ijjxsw.com'+tag.a.get('href'))
            obj = bf(html.read(),'html.parser')
            for tagg in obj.find_all('li'):
                if tagg.a and tagg.a.get_text() == 'txt电子书下载地址【TXT】':
                    down_url.append('https://m.ijjxsw.com'+tagg.a.get('href'))
    return book_name,down_url

def downtoptxt():
    global local_path,logger
    f = open(local_path+'/txt_id.txt','r')
    for i in f.readlines():
        url = 'http://www.zxcs.me/download.php?id='+i
        book_name,down_url = down_zxcs(url)
        recode = download(down_url,book_name)
        print(i.replace('\n',''),book_name,recode)
        logger.write(book_name+'\t'+str(down_url)+recode+'\n')
        time.sleep(5)
        break
    logger.close()

def search_book(_book_name_):
    global local_path,logger
    print('==========开始检索书名 <{0}> (in zxcs.me && kenshu.com)'.format(_book_name_))
    # search in zxcs.me
    url = 'http://www.zxcs.me/index.php?keyword='+quote('《'+_book_name_+'》')
    html = urlopen(url)
    obj = bf(html.read(),'html.parser')
    if obj.dt:
        book_name,down_url = down_zxcs('http://www.zxcs.me/download.php?id='+obj.dt.a.get('href').split('post')[1].replace('/',''))
        print('开始下载 ===========> ',book_name,down_url)
        recode = download(down_url,book_name)
        logger.write(book_name+'\t'+str(down_url)+recode+'\n')
        time.sleep(5)
        if recode=='done':logger.close(),exit(1)
    else:
        print('很遗憾知轩藏书未找到该书，请确认书名是否正确。')
    
    #search in kenshu.com
    data = bytes(urlencode({'searchkey': _book_name_}), encoding='utf8')
    url = 'http://www.kenshuzw.com/modules/article/search.php'
    html = urlopen(url,data=data)
    obj = bf(html.read(),'html.parser')
    if obj.h3 and obj.h3.get_text() == _book_name_:
        book_name,down_url = down_ksw('http://m.kenshuzw.com/'+obj.h3.a.get('href'))
        print('开始下载 ===========> ',book_name,down_url)
        recode = download(down_url,book_name)
        logger.write(book_name+'\t'+str(down_url)+recode+'\n')
        time.sleep(5)
        if recode=='done':logger.close(),exit(1)
    else:
        print('很遗憾啃书网未找到该书，请确认书名是否正确。')
    
    # search in ijjxsw.com 
    data = bytes(urlencode({'show': 'writer,title','keyboard':_book_name_,'Submit22':'搜索'}), encoding='utf8')
    url = 'https://m.ijjxsw.com/e/search/index.php'
    html = urlopen(url,data=data)
    obj = bf(html.read(),'html.parser')
    for tag in obj.find_all("div", class_="main"):
        if tag.a.get_text() == _book_name_:
            book_name,down_url = down_ijjxsw('https://m.ijjxsw.com'+tag.a.get('href'))
            print('开始下载 ===========> ',book_name,down_url)
            recode = download(down_url,book_name)
        logger.write(book_name+'\t'+str(down_url)+recode+'\n')
        time.sleep(5)
        if recode=='done':logger.close(),exit(1)
    else:
        print('很遗憾久久小说网未找到该书，请确认书名是否正确。')
    logger.close()

def main():
    parser = argparse.ArgumentParser(description='搜索书并下载或直接下载 zxcstop 榜.')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.3')
    parser.add_argument('-n','--name', help='book name you want')
    args = parser.parse_args()
    if args.name:
        search_book(args.name)
    else:
        in_content = input('===========要下载的是 top 榜单？(y/n)')
        if in_content.lower()=='y':
            downtoptxt()
        else:
            print('bye')
            exit(1)
    print('done')
    


if __name__ == "__main__":
    main()