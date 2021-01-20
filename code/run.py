import codecs
import os
import sys
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()


from scraping.parser import *
from scraping.models import Vacancy, City, Language


parsers = ((rabota, 'https://www.rabota.ru/vacancy/?query=python&sort=relevance'),
           (hh,
            'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'),
           (super_job, 'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4'),
           (work_city, 'https://moskva.gorodrabot.ru/python'),
           )

city = City.objects.filter(slug='moskva').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
	j, e = func(url)
	jobs += j
	errors += e

for job in jobs:
	v = Vacancy(**job, city=city, language=language)
	try:
		v.save()
	except DatabaseError:
		pass

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
