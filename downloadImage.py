#coding=utf-8
import urllib,urllib2
import re
from lxml import etree

path = 'F:\\photos\\'

def eachPage(i):
    url = 'http://www.mm131.com/qingchun/list_1_%d.html'%i
    html = urllib2.urlopen(url).read()
    re1 = re.compile(r'http://www.mm131.com/qingchun/(.*?).html')
    con = re1.findall(html)
    sum =1
    for q in con:
        eachpeople(q)
        print '第 %d 页 %d 个完成!' %(i,sum)
        sum = sum +1
    print '第 %d 页完成!' %i

def getsum(url):
    html = urllib2.urlopen(url).read()
    con = etree.HTML(html)
    content = con.xpath('//span[@class="page-ch"]/text()')
    if len(content)==0:
        print '出现错误:',url
        return 1
    else:
        x = content[0].strip()
        start = x.find(u'共')
        end = x.find(u'页')
        t= x[start+1:end]
        return int(t)



    
def eachpeople(j):
    sumurl = 'http://www.mm131.com/qingchun/'+str(j)+'.html'
    getsumurl = getsum(sumurl)
    for k in range(2,getsumurl+1):
        purl = 'http://img1.mm131.com/pic/'+str(j)+'/'+str(k)+'.jpg'
        picpath = path +str(j)+'_'+str(k)+'.jpg'
        urllib.urlretrieve(purl,picpath)

if __name__ == '__main__':
    for page in range(2,29):
        eachPage(page)
    print 'all download! over'
