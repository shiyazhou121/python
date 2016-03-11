#coding=utf-8
import urllib2
import requests
from lxml import etree
import re

def crawler(url):
    html = requests.get(url).content
    page = etree.HTML(html)
    return page

def download(url):
    page = crawler(url)
    sku = page.xpath('//li[@class="gl-item"]//div/@data-sku')
    for i in sku:
        name_url = 'http://item.jd.com/'+str(i)+'.html'
        price_url = 'http://p.3.cn/prices/get?skuid=J_'+str(i)
        name_page = crawler(name_url)
        jd_name = name_page.xpath('//div[@id="name"]/h1/text()')
        name = jd_name[0].strip()
        price_page = requests.get(price_url).content
        print type(price_page)
        price_re = re.compile(r'"p":"(.*?)","m"')
        price = re.findall(price_re,price_page)
        for j in [name for k in price]:
            print k
            f=open('jd.txt','a+')
            f.write(j.encode('utf-8')+'\n')
            f.write(k+'\n')
            f.close()

for j in range(1,35):
    url = 'http://list.jd.com/list.html?cat=9987%2C653%2C655&page='+str(j)+'&JL=6_0_0'
    download(url)
    print u'第 %d 页下载完毕！' %j
print 'End!'
