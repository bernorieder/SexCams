import csv
import os.path
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://chaturbate.com/'
htmlfile = 'test.html'

if path.exists(htmlfile):
	fh = open(htmlfile,'r')
	htmlcontent = fh.read()
else:
	driver = webdriver.Chrome()
	driver.get(url)

	htmlcontent = driver.page_source

	fh = open(htmlfile,'w')
	fh.write(htmlcontent)

soup = BeautifulSoup(htmlcontent)

#print(soup.prettify())

mylis = soup.findAll('li', {'class': 'room_list_room'})
print(len(mylis))
rooms = []

for myli in mylis:

	print(myli)

	room = {}
	room['name'] = myli.find('a').get('data-room')
	room['subject'] = myli.find('ul', {'class': 'subject'}).text.replace('\n', '')
	room['location'] = myli.find('li', {'class': 'location'}).text
	room['cams'] = myli.find('li', {'class': 'cams'}).text

	rooms.append(room)

print(rooms)

keys = rooms[0].keys()
with open('rooms.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(rooms)