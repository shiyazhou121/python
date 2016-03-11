#coding=utf-8
import urllib2
import re
import json
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd
from xlwt import Workbook
import time

def func(x):
    try:
        x=float(x)
        return isinstance(x,float)
    except ValueError:
        return False

def down(each, j, data):
	url = 'http://www.worldweather.cn/zh/json/'+str(each)+'_zh.xml'
	html = urllib2.urlopen(url).read()
	con = json.loads(html)['city']
	name = con['cityName']
	memName = con['member']['memName']
	data.write(j, 0, name)
	data.write(j, 1, memName)
	data.write(j, 2, each)
	month_list = con['climate']['climateMonth']
	list_len = len(month_list)
	for i in range(list_len):
		#print i['month'],i['minTemp'],i['maxTemp'],i['rainfall'],i['raindays']
		minTemp = month_list[i]['minTemp']
		maxTemp = month_list[i]['maxTemp']
		rainfall = month_list[i]['rainfall']
		raindays = month_list[i]['raindays']
		print month_list[i]['month'], minTemp, maxTemp, rainfall, raindays
		if not func(minTemp):
			minTemp = 0
		if not func(maxTemp):
			maxTemp = 0
		if not func(rainfall):
			rainfall = 0
		if not func(raindays):
			raindays = 0
		data.write(j, 4*i+3, string.atof(minTemp))
		data.write(j, 4*i+4, string.atof(maxTemp))
		data.write(j, 4*i+5, string.atof(rainfall))
		data.write(j, 4*i+6, string.atof(raindays))




if __name__ =='__main__':
	num = 2070
	book = Workbook(encoding = 'gbk')
	sheet1 = book.add_sheet('Sheet 0')
	j = 0
	for point in range(1,num):
		try:
			down(point, j, sheet1)
			j = j+1
		except Exception,e:
			print e
			f = open('climate.txt','a+')
			f.write(str(point)+'\n')
			f.close()
		print 'this is %s finish' %str(point)
	book.save('climate.xls')
	print 'save over'
