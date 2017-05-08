#!/usr/bin/env python
# coding=utf-8

from bs4 import BeautifulSoup

import urllib
import urllib.request
import urllib.parse
import re
import os

file = open("ip.txt","w")

url = 'http://www.amznz.com/china-ip-list/'

html = urllib.request.urlopen(url)
#print(html.read())

soup = BeautifulSoup(html,'lxml')

lines = soup.find_all('p')
i = 0
for line in lines:
    if i == 4:
        #print(line)
        #print(type(line))
        #print(line.get_text())
        hosts0 = line.get_text().split("Korea")[0].split("China")
        for host in hosts0:
            print(host)
            file.write(host+'\n')

        hosts1 = line.get_text().split("Korea")[1].split("China")
        for host in hosts1:
            print(host)
            file.write(host+'\n')

    i += 1

file.close()
