#coding=utf-8
import urllib2,urllib
import cookielib
import requests
import re
import time
import random
from lxml import etree

#b    
obuff = []
for ln in open('jay_people_url.txt'):
    if ln in obuff:
        continue
    obuff.append(ln)
with open('b.txt', 'w') as handle:
    handle.writelines(obuff)

#d
lines_seen = set() 
outfile = open("d.txt", "w")
for line in open("jay_people_url.txt", "r"):
    if line not in lines_seen: 
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

