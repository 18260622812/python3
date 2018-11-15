# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('E:\\2\\host\\10.192.72.201.html','rb'),"html.parser")
#print(soup.prettify())
items = soup.find_all('table',attrs={'class':'report_table','style':'word-wrap:break-word;'})
for child in items[0].tbody.descendants:
    print(child)
#print(items[0].tbody)
#dd=soup.find(text="")
#print(dd)