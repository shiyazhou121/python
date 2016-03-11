#coding=utf-8
import urllib2
import time
import json
from lxml import etree

#爬虫
def crawler(url):
    html = urllib2.urlopen(url).read()
    return html

#得到播放量
def get_play_index(name):
    url = 'http://uaa.iqiyi.com/video_index/v1/get_index_trend?album_name='+name+'&time_window=90&callback=window.Q.__callbacks__.cbquyvm0'
    html = crawler(url)
    start = html.find('"data":{')
    med = html.find('{',start+8)
    end = html.find('}',start)
    data = html[med:end+1]
    json_data = json.loads(data)
    return repr(json_data)


#得到播放设备比(电脑、手机)     
def get_device(name):
    url = 'http://index.iqiyi.com/q/?name='+name
    html = crawler(url)
    con = etree.HTML(html)
    mobile_device = con.xpath('//div[@class="dev_ct fl pr"]//span/text()')
    return ','.join(mobile_device)

#得到各省播放量:"北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省","吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区","海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区","台湾","香港特别行政区","澳门特别行政区"
def get_province(name):
    url = 'http://uaa.iqiyi.com/video_index/v1/get_province_distribution?album_name='+name+'&callback=window.Q.__callbacks__.cbbukqtw'
    html = crawler(url)
    start = html.find('"details":{')
    med = html.find('{',start+2)
    end = html.find('}',start)
    data = html[med:end+1]
    json_data = json.loads(data)
    deal_data = json_data.values()
    med = map(str,deal_data[0])
    return ','.join(med)



#得到用户画像 性别、年龄、星座、文化水平、兴趣分布
def get_much(name):
    url = 'http://uaa.iqiyi.com/video_index/v1/get_user_profile?album_name='+name+'&callback=window.Q.__callbacks__.cbfqq0t3'
    html = crawler(url)
    start = html.find('"details":{')
    med = html.find('{',start+11)
    end = html.find('}',start)
    data = html[med:end+1]
    json_data = json.loads(data)
    #得到性格比
    gender = deal(json_data["gender"])
    #得到年龄分布
    age = deal(json_data["age"])
    #得到星座分布
    constellation = deal(json_data["constellation"])
    #得到教育水平分布
    education = deal(json_data["education"])
    #得到兴趣分布
    interest = deal(json_data["interest"])
    return gender+'|'+age+'|'+constellation+'|'+education+'|'+interest

def get_all(name):
    #播放量按照字典储存
    index = get_play_index(name)
    #设备按照字符串储存，中间用，分割
    device = get_device(name)
    #得到省会：以，分割
    province = get_province(name)
    #得到用户画像，以，分割，以|分组
    much = get_much(name)
    return index+'|'+device+'|'+province+'|'+much

#将列表转化成字符串，并以，分割
def deal(data):
    strr = map(str,data)
    con = ','.join(strr)
    return con

