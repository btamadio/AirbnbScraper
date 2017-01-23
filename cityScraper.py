#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class cityScraper:
    def __init__(self,cityName):
        self.roomList = []
        for room_type in ['Entire%20home%2Fapt','Private%20room','Shared%20room']:
            url = 'https://www.airbnb.com/s/'+cityName+'?room_types[]='+room_type
            req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
            mainPage = urlopen(req).read()
            mainSoup = BeautifulSoup(mainPage,"lxml")
            all_links = mainSoup.find_all('a')
            for link in all_links:
                href = link.get('href')
                if href:
                    if '/rooms/' in href and not 'new?' in href:
                        roomNum = int(href.split('/')[2])
                        if not roomNum in self.roomList:
                            self.roomList.append(roomNum)

c = cityScraper('San-Francisco--CA')
print(len(c.roomList))
