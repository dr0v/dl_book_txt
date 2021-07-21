# 简单说明
简单解析了两个友好的网站： zxcs.me 和 kenshuzw.com 进行txt 书下载。

## 原理
1. zxcs

书籍搜索| http://www.zxcs.me/index.php?keyword=
--|--
书籍下载|http://www.zxcs.me/download.php?id=

2. 啃书网

书籍搜索| http://www.kenshuzw.com/modules/article/search.php
--|--
书籍下载|http://txt.kenshuzw.com/modules/article/txtarticlee.php?

## 脚本依赖

```
pip install bs4
pip install rarfile
```

## 脚本使用方法

批量下载(从 txt_id.txt 中)： python downtxt.py

检索书名下载：python downtxt.py -n 书名