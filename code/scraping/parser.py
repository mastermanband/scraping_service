import requests
import codecs
from bs4 import BeautifulSoup as Bs
from random import randint

__all__ = ('rabota', 'hh', 'work_city', 'super_job')

header = [
	{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
	 'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
	{'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 2 XL Build/PPP3.180510.008) AppleWebKit/537.36 '
	               '(KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
	 'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
	{'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 '
	               '(KHTML, like Gecko) Version/4.0 Chrome/71.1.2222.33 Mobile Safari/537.36',
	 'Accept': 'text/html,applications/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
]


def rabota(url):
	jobs = []
	errors = []
	domain = 'https://www.rabota.ru'
	resp = requests.get(url, headers=header[randint(0, 2)])
	if resp.status_code == 200:
		soup = Bs(resp.content, 'html.parser')
		main_div = soup.find('div', attrs={'class': 'r-serp'})
		if main_div:
			div_list = main_div.find_all('div', class_='vacancy-preview-card__top')
			for div in div_list:
				title = div.find('h3')
				title_url = title.a['href']
				description = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
				company = 'No name'
				c = div.find('div', class_='vacancy-preview-card__company')
				if c:
					company = c.a.text
				jobs.append({
					'title': title.text, 'url': domain + title_url, 'description': description, 'company': company
				})
		else:
			errors.append({'url': url, 'title': "Div does not exists"})
	else:
		errors.append({'url': url, 'title': "Page do not response"})
	return jobs, errors


def hh(url):
	resp = requests.get(url, headers=header[randint(0, 2)])
	jobs = []
	errors = []
	if resp.status_code == 200:
		soup = Bs(resp.content, 'html.parser')
		main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
		if main_div:
			div_list = main_div.find_all('div', class_='vacancy-serp-item')
			for div in div_list:
				title = 'text'
				t = div.find('div', class_='vacancy-serp-item__row vacancy-serp-item__row_header')
				if t:
					title = t.a.text
				title_url = t.a['href']
				description = div.find('div', attrs={'class': 'g-user-content'}).text
				company = 'No name'
				# city = div.find('div', class_='vacancy-serp-item__meta-info').text
				# language = div.find()
				c = div.find('div', class_='vacancy-serp-item__meta-info-company')
				if c:
					company = c.a.text
				jobs.append({
					'title': title, 'url': title_url, 'description': description, 'company': company,
				})
		else:
			errors.append({'url': url, 'title': "Div does not exists"})
	else:
		errors.append({'url': url, 'title': "Page do not response"})
	return jobs, errors


def work_city(url):
	resp = requests.get(url, headers=header[randint(0, 2)])
	jobs = []
	errors = []
	if resp.status_code == 200:
		soup = Bs(resp.content, 'html.parser')
		main_div = soup.find('div', attrs={'class': 'result-list'})
		if main_div:
			div_list = main_div.find_all('div', class_='snippet__inner')
			for div in div_list:
				title = div.find('h2')
				title_url = title.a['href']
				description = div.find('div', class_='snippet__desc').text
				company = div.find('li', class_='snippet__meta-item snippet__meta-item_company').text
				jobs.append({
					'title': title.text, 'url': title_url, 'description': description, 'company': company,
				})
		else:
			errors.append({'url': url, 'title': "Div does not exists"})
	else:
		errors.append({'url': url, 'title': "Page do not response"})
	return jobs, errors


def super_job(url):
	domain = 'https://www.superjob.ru'
	resp = requests.get(url, headers=header[randint(0, 2)])
	jobs = []
	errors = []
	if resp.status_code == 200:
		soup = Bs(resp.content, 'html.parser')
		main_div = soup.find('div', attrs={'class': '_1ID8B'})
		if main_div:
			div_list = main_div.find_all('div', class_='Fo44F QiY08 LvoDO')
			for div in div_list:
				title = div.find('div', class_='_3mfro PlM3e _2JVkc _3LJqf')
				title_url = title.a['href']
				description = div.find('div', class_='HSTPm _3C76h _10Aay _2_FIo _1tH7S').text
				company = div.find('span',
				                   class_='_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI').text
				jobs.append({
					'title': title.text, 'url': domain + title_url, 'description': description, 'company': company,
				})
		else:
			errors.append({'url': url, 'title': "Div does not exists"})
	else:
		errors.append({'url': url, 'title': "Page do not response"})
	return jobs, errors


if __name__ == '__main__':
	url = 'https://www.rabota.ru/vacancy/?query=python&sort=relevance'
	jobs, errors = rabota(url)
	h = codecs.open('test.txt', 'w', 'utf-8')
	h.write(str(jobs))
	h.close()
