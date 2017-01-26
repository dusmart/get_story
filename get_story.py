# -*- coding:utf-8 -*
"""get all download url from given url"""
from time import sleep
import os
import sys
import urllib
import re
import requests

def geturl(name):
    """main function"""
    website = "http://www.520tingshu.com"
    payload = {'searchword':name.decode('utf8').encode('gbk'), 'Submit':''}
    req = requests.post(website + "/search.asp", data=payload)
    text = req.content.decode('gbk').encode('utf8')
    #filex = open("1.html", 'w')
    #filex.write(text.decode('utf8').encode('gbk'))
    book_reg = r'<h2><a href="\/book\/book(\d+).html" title=".*">.*<\/a><\/h2>'
    #e.g. <h2><a href="/book/book14675.html" title="老九门的那些事">老九门的那些事</a></h2>
    books = re.findall(book_reg, text)
    if len(books) == 0:
        print "对不起，没有这本书，是否有拼写错误"
        return
    else:
        print "搜到" + str(len(books)) + "本书，默认下载第一本"
        book_url = website + "/video/?" + books[0] + "-0-0.html"
    #print book_url


    book_page = requests.get(book_url).content.decode('gbk').encode('utf8')
    playdata_reg = r'<script src="(/playdata.*\.js)">'
    playdata = re.findall(playdata_reg, book_page)
    #print playdata
    playdata = website + playdata[0]
    play_link = requests.get(playdata).content.decode('unicode_escape').encode('utf8')
    #print play_link

    download_reg = r"\$(http.*?)\$flv',"
    downloads = re.findall(download_reg, play_link)

    if len(downloads) == 0:
        print "资源拒绝访问，无法下载"
        return
    try:
        os.mkdir(name)
    except OSError:
        pass

    total = len(downloads)
    for index, download in enumerate(downloads):
        if index%(total/10) == 0:
            print str(index) + "集已下载 总共" + str(total) + "集"
        path = name + download[download.rfind('/'):]
        urllib.urlretrieve(download, path)
        assert os.path.getsize(path) > 10000


if __name__ == "__main__":
    try:
        geturl(sys.argv[1])
    except requests.exceptions.ConnectionError:
        sleep(0.5)
        try:
            geturl(sys.argv[1])
        except requests.exceptions.ConnectionError:
            print "请检查网络状况"

