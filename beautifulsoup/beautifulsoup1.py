
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('E:\\3\\report.html','rb'),"html.parser")
#print(soup.prettify())
items = soup.find_all('table',attrs={'class':'report_table '})
print(len(items))
print(items[0])
#dd=soup.find(text="")
#print(dd)
