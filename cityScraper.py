#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import pprint
import json

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
        for room_type in ['Private%20room']:#['Entire%20home%2Fapt','Private%20room','Shared%20room']:
            for (price_min,price_max) in [(0,50),(51,75),(76,100),(101,150),(151,200),(201,300),(301,-1)]:
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
            writer = csv.writer(csvFile,delimiter=';')
            headers = ['roomID','acc_rating','bed_type','cancel_policy','checkin_rating','cleanliness_rating','communication_rating','guest_sat','hosting_id','instant_book','is_superhost','loc_rating','lat','lon','page','person_cap','pic_count','room_type','saved_to_wishlist_count','value_rating','rev_count','price','star_rating']
            for i in range(1,51):
                headers.append('amen'+str(i))
            writer.writerow(headers)
            for room in self.roomList:
                line = self.scrapeRoom(room)
                if len(line) > 0:
                    writer.writerow(line)
    def scrapeRoom(self,roomNum):
        url = 'https://www.airbnb.com/rooms/'+roomNum
        print('Scraping room info from ',url)
        try:
            req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page,"lxml")
            star_rating = soup.find('div',class_='star-rating').get('content')
            meta = soup.find('meta',id='_bootstrap-room_options')
            if not meta:
                return []
            dict0 = json.loads(meta.get('content'))
            if not dict0:
                return []
            dataDict = dict0['airEventData']
            if dataDict:
                acc_rating = dataDict['accuracy_rating']
                amenList = dataDict['amenities']
                bed_type = dataDict['bed_type']
                cancel_policy = dataDict['cancel_policy']
                checkin_rating = dataDict['checkin_rating']
                cleanliness_rating = dataDict['cleanliness_rating']
                communication_rating = dataDict['communication_rating']
                guest_sat = dataDict['guest_satisfaction_overall']
                hosting_id = dataDict['hosting_id']
                instant_book = dataDict['instant_book_possible']
                is_superhost = dataDict['is_superhost']
                loc_rating = dataDict['location_rating']
                lat = dataDict['listing_lat']
                lon = dataDict['listing_lng']
                page = dataDict['page']
                person_cap = dataDict['person_capacity']
                pic_count = dataDict['picture_count']
                price = dataDict['price']
                room_type = dataDict['room_type']
                saved_to_wishlist_count = dataDict['saved_to_wishlist_count']
                value_rating = dataDict['value_rating']
                rev_count = dataDict['visible_review_count']
                featureVec = [roomNum,acc_rating,bed_type,cancel_policy,checkin_rating,cleanliness_rating,communication_rating,guest_sat,hosting_id,instant_book,is_superhost,loc_rating,lat,lon,page,person_cap,pic_count,room_type,saved_to_wishlist_count,value_rating,rev_count,price,star_rating]
                for i in range(1,51):
                    featureVec.append(i in amenList)
                return featureVec
            else:
                return []
        except:
            return []
c = cityScraper('San-Francisco--CA')
c.getRoomList()
c.scrapeRooms('SF_roomlist_private.txt','SF_data_private.csv')

print(len(c.roomList))
