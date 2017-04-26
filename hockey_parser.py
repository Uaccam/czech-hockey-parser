import urllib.request
import csv
from bs4 import BeautifulSoup

base_url = 'http://www.hokej.cz/tipsport-extraliga/zapasy?matchList-view-displayAll=1&matchList-filter-season=2016&matchList-filter-competition=5821'
matches = []

def get_html(url):
	response = urllib.request.urlopen(url)
	return response.read()

def parse(html):
	soup = BeautifulSoup(html)
	tables = soup.find_all('table', class_='preview m-b-30')
	for table in tables:
		rows = table.find_all('tr')
		for row in rows:
			try:
				templist = []
				cols = row.find_all('td')[1:6]


				name1 = cols[0].find('span', class_='preview__name--long')
				templist.append(name1.text)

				score1 = cols[1].find('span', class_='blue')
				templist.append(score1.text)

				starttime = cols[2].find('span', class_='match-start-time')
				templist.append(starttime.text)

				score2 = cols[3].find('span')
				templist.append(score2.text)

				name2 = cols[-1].find('span', class_='preview__name--long')
				templist.append(name2.text)

				matches.append(templist)

			except(AttributeError):
				pass


def save(matches, path):
	with open(path, 'w', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		for match in matches:
			if match[0] == "HC VÍTKOVICE RIDERA" or match[-1] == "HC VÍTKOVICE RIDERA":
				writer.writerow(match)


def main():
	parse(get_html(base_url))
	save(matches, 'matches.csv')



if __name__ == '__main__':
	main()