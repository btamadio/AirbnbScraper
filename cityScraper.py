#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

class cityScraper:
    def __init__(self,cityName):
        self.roomList = []
        self.cityName = cityName
        self.roomListFile = open('newRoomList.txt','w')
    def getURL(self,room_type,price_min,price_max,page_num):
        if price_max > 0:
            url= 'https://www.airbnb.com/s/'+self.cityName+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&price_max='+str(price_max)+'&page='+str(page_num)
        else:
            url= 'https://www.airbnb.com/s/'+self.cityName+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&page='+str(page_num)
        print(url)
        return url
    def getRooms(self,pageNum):
        for room_type in ['Entire%20home%2Fapt','Private%20room','Shared%20room']:
            for (price_min,price_max) in [(0,100),(101,200),(201,300),(301,-1)]:
                req = Request(self.getURL(room_type,price_min,price_max,pageNum),headers={'User-Agent':'Mozilla/5.0'})
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
        pageNum = 1
        addedRoom = True
        while addedRoom:
            addedRoom = False
            for roomNum in self.getRooms(pageNum):
                if roomNum not in self.roomList:
                    self.roomList.append(roomNum)
                    self.roomListFile.write(str(roomNum)+'\n')
                    addedRoom = True
            pageNum+=1
        self.roomListFile.close()
    def scrapeRooms(self,roomListFile,outputFile):
        self.roomList = []
        with open(roomListFile) as f:
            for line in f:
                self.roomList.append(line.rstrip())
        with open(outputFile,'w') as csvFile:
            writer = csv.writer(csvFile,delimiter=',')
            for room in self.roomList[0:3]:
                line = self.scrapeRoom(room)
                writer.writerow(line)
    def scrapeRoom(self,roomNum):
        url = 'https://www.airbnb.com/rooms/'+roomNum
        print('Scraping room info from ',url)
        req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page,"lxml")
        lat = soup.find('meta',property='airbedandbreakfast:location:latitude').get('content')
        lon = soup.find('meta',property='airbedandbreakfast:location:longitude').get('content')
        featureVec = [lat,lon]
        return featureVec
        
c = cityScraper('San-Francisco--CA')
c.scrapeRooms('SF_roomlist.txt','SF_data.csv')
#c.getRoomList()
#print(len(c.roomList))
