import csv
import datetime
import time
import os.path
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://chaturbate.com'
filename = 'files/test_' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')


def getPage(url,counter,scrapetime):

	global nopages

	driver.get(url)

	"""
	if path.exists(htmlfile):
		fh = open(htmlfile,'r')
		htmlcontent = fh.read()
	else:
	"""

	htmlcontent = driver.page_source

	# write HTML file
	fh = open(filename + '_' + str(counter) + '.html','w')
	fh.write(htmlcontent)

	# parse HTML
	soup = BeautifulSoup(htmlcontent)

	#print(soup.prettify())

	if len(rooms) == 0:
		tmp = soup.findAll('a', {'class': 'endless_page_link'})
		nopages = tmp[len(tmp)-2].text

	mylis = soup.findAll('li', {'class': 'room_list_room'})
	print(len(mylis))

	# process each room box
	for myli in mylis:

		print(myli)

		room = {}
		room['position'] = len(rooms)
		room['name'] = myli.find('a').get('data-room')
		room['subject'] = myli.find('ul', {'class': 'subject'}).text.replace('\n', '')
		room['location'] = myli.find('li', {'class': 'location'}).text

		tmp = myli.find('li', {'class': 'cams'}).text.replace(' ','')
		tmp = tmp.split(',')
		room['viewers'] = tmp[1].replace('viewers', '')
		room['time'] = tmp[0]
		if "hrs" in room['time']:
			room['time'] = round(float(room['time'].replace('hrs','')) * 60)
		else:
			room['time'] = float(room['time'].replace('mins','').replace('min', ''))

		tmp = myli.find('div', {'class': 'title'}).find('span')
		room['age'] = tmp.text
		room['gender'] = tmp.attrs['class'][1]

		room["thumbnail_label"] = myli.find('div', {'class': 'thumbnail_label'}).text

		room['scrapetime'] = scrapetime

		rooms.append(room)

	try:
		# get the link to the next page from the next button
		next_button = driver.find_element_by_class_name('next')
		nextlink = next_button.get_attribute('href')
	except:
		print("captcha at " + str(counter))
		return False

	print(nextlink)

	if nextlink.endswith('#'):
		return False
	else:
		return nextlink

#script starts here
driver = webdriver.Chrome()
rooms = []
nopages = 0

counter = 0
nextstep = url

while nextstep is not False:
	nextstep = getPage(nextstep,counter,datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
	counter += 1
	#break
	time.sleep(10)

csvfilename = filename + '_' + nopages + 'pages.csv'
keys = rooms[0].keys()
with open(csvfilename, 'w', newline='')  as output_file:
	dict_writer = csv.DictWriter(output_file, keys)
	dict_writer.writeheader()
	dict_writer.writerows(rooms)

driver.quit()