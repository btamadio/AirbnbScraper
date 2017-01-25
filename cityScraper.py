#!/usr/bin/env python
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import pprint
import json

class cityScraper:
    def __init__(self):
        pass
    def getLastPage(self,city_name,room_type,price_min,price_max):
        url = self.getURL(city_name,room_type,price_min,price_max,1)
        req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page,"lxml")
        lastPage = 1
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            if '/s/'+city_name+'?page=' in href:
                pageLink = int(href.split('=')[1])
                if pageLink > lastPage:
                    lastPage = pageLink
        return lastPage
    def scrapeRoomIDs(self,city_name,room_type):
        for (price_min,price_max) in [(0,40),(41,45),(46,50),(51,55),(56,59),(60,61),(62,63),(64,65),(66,68),(69,70),(71,73),(74,75),(76,78),(79,80),(81,85),(86,90),(91,95),(96,100),(101,150),(151,200),(201,-1)]:
            lastPage = self.getLastPage(city_name,room_type,price_min,price_max)
            for page_num in range(1,lastPage+1):
                url = self.getURL(city_name,room_type,price_min,price_max,page_num)
                print('scraping room IDs from %s' % url)
                req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
                page = urlopen(req).read()
                soup = BeautifulSoup(page,"lxml")
                all_links = soup.find_all('a')
                for link in all_links:
                    href = link.get('href')
                    if href:
                        if '/rooms/' in href and not 'new?' in href:
                            room_id = int(href.split('/')[2])
                            yield str(room_id)
    def getURL(self,city_name,room_type,price_min,price_max,page_num):
        if price_max > 0:
            url= 'https://www.airbnb.com/s/'+city_name+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&price_max='+str(price_max)+'&page='+str(page_num)
        else:
            url= 'https://www.airbnb.com/s/'+city_name+'?room_types[]='+room_type+'&price_min='+str(price_min)+'&page='+str(page_num)
        return url
    def writeRoomIDs(self,city_name,room_type,out_file):
        f = open(out_file,'w')
        idList = []
        for roomID in self.scrapeRoomIDs(city_name,room_type):
            if not roomID in idList:
                idList.append(roomID)
                f.write(roomID+'\n')
    def scrapeRooms(self,room_file,out_file):
        room_list = []
        with open(room_file) as f:
            for line in f:
                room_list.append(line.rstrip())
        with open(out_file,'w') as csvFile:
            writer = csv.writer(csvFile,delimiter=';')
            headers = ['room_id','acc_rating','bed_type','cancel_policy','checkin_rating',
                       'cleanliness_rating','communication_rating','guest_sat','hosting_id',
                       'instant_book','is_superhost','loc_rating','lat','lon','page','person_cap',
                       'pic_count','room_type','saved_to_wishlist_count','value_rating','rev_count','price','star_rating']
            for i in range(1,51):
                headers.append('amen_'+str(i))
            writer.writerow(headers)
            for room_id in room_list:
                line = self.scrapeRoom(room_id)
                if len(line) > 0:
                    writer.writerow(line)                
    def scrapeRoom(self,room_id):
        url = 'https://www.airbnb.com/rooms/'+room_id
        print('Scraping room info from ',url)
        try:
            req = Request(url,headers={'User-Agent':'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page,"lxml")
            star_rating = 0
            star_rating_tag = soup.find('div',class_='star-rating')
            if star_rating_tag:
                star_rating=star_rating_tag.get('content')
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
                featureVec = [room_id,acc_rating,bed_type,cancel_policy,checkin_rating,cleanliness_rating,communication_rating,guest_sat,hosting_id,instant_book,is_superhost,loc_rating,lat,lon,page,person_cap,pic_count,room_type,saved_to_wishlist_count,value_rating,rev_count,price,star_rating]
                for i in range(1,51):
                    featureVec.append(i in amenList)
                return featureVec
            else:
                return []
        except:
            return []

