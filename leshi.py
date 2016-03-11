#coding=utf-8
import urllib2
import re
import time
from lxml import etree

global count
count = 1

def crawler(url):
    html = urllib2.urlopen(url).read()
    return html

def deal(data):
    if len(data)==0:
        return ''
    elif len(data)==1:
        return data[0].strip().encode('utf-8')
    else:
        z = ' '.join(data)
        return z.encode('utf-8')

def geturl(url):
    con = crawler(url)
    req = re.compile('href="http://list.letv.com/listn/(.*?).html')
    content = re.findall(req,con)
    return content

def getcontent(url,areaNum,Szz):
    con1 = crawler(url)
    con2 = etree.HTML(con1)
    con = con2.xpath('//dd[@class="dd_cnt"]')
    print len(con)
    for i in range(len(con)):
        name1 = con[i].xpath('p[@class="p_t"]/a/text()')
        name = name1[0].strip().encode('utf-8')
        performer1 = con[i].xpath('p[@class="p_c"]/a/text()')
        performer = deal(performer1)
        style1 = con[i].xpath('p/span[@class="mr0"]/text()')
        style = deal(style1)
        area1 = con[i].xpath('p//span[@class="area"]/text()')
        area = deal(area1)
        time1 = con[i].xpath('p//span[@class="release_date"]/text()')
        time = deal(time1)
        pingfen1 = con[i].xpath('p[@class="p_c ico_num"]/em/text()')
        pingfen = deal(pingfen1)
        play1 = con[i].xpath('p[@class="p_c ico_num"]/span[@class="ico_play_num"]/text()')
        play = deal(play1)
        total1 = name.replace('|',' ')+'|'+performer.replace('|',' ')+'|'+style.replace('|',' ')+'|'+area.replace('|',' ')+'|'+time.replace('|',' ')+'|'+pingfen.replace('|',' ')+'|'+play.replace('|',' ')
        if areaNum == '1':
            areaname = '内地'
        elif areaNum =='2':
            areaname = '香港'
        else:
            areaname = '台湾'
        total = areaname +'|'+ Szz +'|'+ total1
        f = open('leshi.txt','a+')
        f.write(total+'\n')
        f.close()
        global count
        print 'this is end!:%d:%d' %(count,i)
        count = count + 1
        
if __name__=='__main__':
    str1 = ['2015','2014','2013','2012','2011','2010','00s','90s','0']
    areanum = ['1','2','3']
    for k in areanum:
        for i in str1:
            try:
                url = 'http://list.letv.com/listn/c1_t-1_a5000%s_y%s_s1_lg-1_ph-1_md_o4_d1_p.html' %(k,i)
                eachurl111 = geturl(url)
                if len(eachurl111)==0:
                    print 'no page!'
                    kk = url.find('listn/')
                    end = url.find('.html',kk)
                    z = url[kk+6:end]
                    eachurl = [z]
                    print eachurl
                else:
                    eachurl = eachurl111
                for j in eachurl:
                    newurl = 'http://list.letv.com/listn/'+j+'.html'
                    print newurl
                    getcontent(newurl,k,i)
                    print 'page is end!'
                    time.sleep(1)
            except Exception,msg:
                print msg
                print type(msg)
                f = open('leishi_error.txt','a+')
                global count
                f.write(str(count)+'\n')
                f.close() 
            print 'this %s is end!' %i
        print 'this area is end!:%s' %k
    print 'all is end!'




    
