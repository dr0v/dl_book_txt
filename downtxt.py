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

from cmath import e
from email import header
from hashlib import new
import os,sys,time,random
import argparse
from urllib import response
from urllib.parse import quote,urlencode
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bf
import requests
import rarfile
import tempfile

local_path = os.path.dirname(os.path.realpath(__file__))
logger = open(local_path+'/log.txt','a+')
USER_AGENTS = [
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
 "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
 "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
 "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
 "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

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
    random_agent = USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]
    header = {
        'user-agent': random_agent,
        'Referer': 'www.baidu.com'
    }
    # search in zxcs.me
    url = 'http://www.zxcs.me/index.php?keyword='+quote(_book_name_)#'《'+_book_name_+'》')
    try:
        req = Request(url,headers=header)
        html = urlopen(req).read()
        obj = bf(html,'html.parser')
        if obj.dt:
            dt_list = obj.find_all("dt")
            for dt in dt_list:
                if dt.a and _book_name_ in dt.a.get_text().split('》')[0]:obj.dt = dt;break
            book_name,down_url = down_zxcs('http://www.zxcs.me/download.php?id='+obj.dt.a.get('href').split('post')[1].replace('/',''))
            print('开始下载 ===========> ',book_name,down_url)
            recode = download(down_url,book_name)
            logger.write(book_name+'\t'+str(down_url)+recode+'\n')
            if recode=='done':logger.close(),exit(1)
        else:
            print('很遗憾知轩藏书未找到该书，请确认书名是否正确。')
    except:
        print('error ============> \n', sys.exc_info())
    
    #search in kenshu.com
    data = bytes(urlencode({'searchkey': _book_name_}), encoding='utf8')
    url = 'http://www.kenshuzw.com/modules/article/search.php'
    try:
        req = Request(url,data=data,headers=header)
        html = urlopen(req).read()
        obj = bf(html,'html.parser')
        if obj.h3 and obj.h3.get_text() == _book_name_:
            book_name,down_url = down_ksw('http://m.kenshuzw.com/'+obj.h3.a.get('href'))
            print('开始下载 ===========> ',book_name,down_url)
            recode = download(down_url,book_name)
            logger.write(book_name+'\t'+str(down_url)+recode+'\n')
            if recode=='done':logger.close(),exit(1)
        else:
            print('很遗憾啃书网未找到该书，请确认书名是否正确。')
    except:
        print('error ============> \n', sys.exc_info())
    
    # search in ijjxsw.com 
    data = bytes(urlencode({'show': 'writer,title','keyboard':_book_name_,'Submit22':'搜索'}), encoding='utf8')
    url = 'https://m.ijjxsw.com/e/search/index.php'
    try:
        req = Request(url,data=data,headers=header)
        html = urlopen(req).read()
        obj = bf(html,'html.parser')
        for tag in obj.find_all("div", class_="main"):
            if _book_name_ in tag.a.get_text() :
                book_name,down_url = down_ijjxsw('https://m.ijjxsw.com'+tag.a.get('href'))
                print('开始下载 ===========> ',book_name,down_url)
                recode = download(down_url,book_name)
                logger.write(book_name+'\t'+str(down_url)+recode+'\n')
                if recode=='done':logger.close(),exit(1)
        else:
            print('很遗憾久久小说网未找到该书，请确认书名是否正确。')
    except:
        print('error ============> \n', sys.exc_info())
    logger.close()

def main():
    parser = argparse.ArgumentParser(description='搜索书并下载或直接下载 zxcstop 榜.')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.3')
    parser.add_argument('-n','--name', help='book name you want')
    args = parser.parse_args()
    if args.name:
        search_book(args.name)
    else:
        in_content = input('===========要下载的是 top 榜单？(y/n)\t')
        if in_content.lower()=='y':
            downtoptxt()
        else:
            print('bye')
            exit(1)
    print('done')
    


if __name__ == "__main__":
    main()