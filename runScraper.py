#!/usr/bin/env python
from cityScraper import cityScraper
c=cityScraper()
#c.writeRoomIDs('San-Francisco--CA','Private%20room','test.txt')
c.scrapeRooms('data/SF_roomList_private_2.txt','data/SF_data_private_2.csv')
