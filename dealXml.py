#coding=utf-8
import xml.dom.minidom
import csv
import os

class dealXml(object):

	def __init__(self, path):
		self.path = path

	def getFile(self):
		Files = os.listdir(self.path)
		FileList = []
		for each in Files:
			point = each.find('.pdml')
			if point != -1:
				FileList.append(each[:point])
		return FileList

	def deal(self):
		FileList = self.getFile()
		count = 1
		for each_path in FileList:
			csvFile = file(self.path+'\\'+each_path+'.csv','wb')
			writer = csv.writer(csvFile)
			writer.writerow(['host','uri'])
			doc = xml.dom.minidom.parse(self.path+'\\'+each_path+'.pdml')
			packet = doc.documentElement
			protos = packet.getElementsByTagName('proto')
			need = {}
			for proto in protos:
				fields = proto.getElementsByTagName('field')
				key = ''
				value = ''
				for field in fields:
					if field.getAttribute('name') =='http.host':
						key = field.getAttribute('show')
					if field.getAttribute('name') =='http.request.uri':
						value = field.getAttribute('show')
				if len(key)!=0 and '.' in key:
					a = []
					print key
					a.append(key)
					a.append(value)
					writer.writerow(a)
					
			print 'this %d is over!' %count
			count += 1



a = dealXml('C:\\Users\\sky\\Desktop\\dataSet')
a.deal()