#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class cityScraper:
    def __init__(self,cityName):
        self.roomList = []
        self.cityName = cityName
    def getURL(self,room_type,price_min,price_max,page_num):
        if price_max > 0:
            url= 'https://www.airbnb.com/s/'+self.cityName+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&price_max='+str(price_max)+'&page='+str(page_num)
        else:
            url= 'https://www.airbnb.com/s/'+self.cityName+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&page='+str(page_num)
        print(url)
        return url
    def getLinks(self):
        for room_type in ['Entire%20home%2Fapt','Private%20room','Shared%20room']:
            for (price_min,price_max) in [(0,100),(101,200),(201,300),(301,-1)]:
                req = Request(self.getURL(room_type,price_min,price_max,1),headers={'User-Agent':'Mozilla/5.0'})
                mainPage = urlopen(req).read()
                mainSoup = BeautifulSoup(mainPage,"lxml")
                all_links = mainSoup.find_all('a')
                for link in all_links:
                    href = link.get('href')
                    if href:
                        if '/rooms/' in href and not 'new?' in href:
                            roomNum = int(href.split('/')[2])
                            yield roomNum
    def getRoomList(self):
        for roomNum in self.getLinks():
            if roomNum not in self.roomList:
                self.roomList.append(roomNum)
c = cityScraper('San-Francisco--CA')
c.getRoomList()
print(c.roomList)
