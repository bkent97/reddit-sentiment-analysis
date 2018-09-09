import requests
import time
import random
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
url = "http://www.amazon.com"
links = []
reviewBodies = []
reviewRatings = []

try:
	f = open("amazonLinks.txt", "r")
	lines = f.read().splitlines()
	for line in lines:
		links.append(line)
	f.close()
	random.shuffle(links)
except:
	print("no links file found")


for n in range(1,100):
	url = links[n]
	print(url)
	time.sleep(3)
	page = requests.get(url,headers = headers,verify=False)
	soup = BeautifulSoup(page.content,'html.parser')

	for item in soup.find_all('a', href=True):
		if "show_all_top" in str(item['href']):
			url = "http://www.amazon.com" + str(item['href'])
			pagenum = 1
			number_of_pages = random.randint(2, 6)
			for pnum in range(1, number_of_pages):
				wait_time = random.randint(8, 14)
				time.sleep(wait_time)
				pagenum += 1
				newpage = "pageNumber=" + str(pagenum) 
				reviewsPage = requests.get(url,headers = headers,verify=False)
				reviewsSoup = BeautifulSoup(reviewsPage.content, 'html.parser')

				for x in reviewsSoup.find_all('span'):
					if 'data-hook="review-body"' in str(x):
						bodyInd = 62
						body = ""
						while bodyInd < (len(str(x)) - 7):
							body += str(x)[bodyInd]
							bodyInd += 1

#					print(body) 					
						reviewBodies.append(body)


				for review in reviewsSoup.find_all('a',href=True):
			#	print(review)
					if "customer-reviews" in str(review['href']):
#					print("found a link normal")
						rating = str(review.get('title')).split(' ')[0]
						if rating != "None":
			#			print(review, "\n", rating)
							reviewRatings.append(rating)
			
					if newpage in str(review['href']):
						url = "http://www.amazon.com" + str(review['href'])

ind = 0
print("reviewRatings length: ", len(reviewRatings))
print("reviewBodies length: ", len(reviewBodies))

f = open("amazon06-25.txt", "w")
while ind < len(reviewRatings):	
	line = reviewRatings[ind] + ":" + reviewBodies[ind] + "\n"
	f.write(line)
	ind += 1
