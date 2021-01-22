import jsonfield as jsonfield
from django.db import models

from scraping.utils import from_cyrillic_to_eng


def default_urls():
	return {'rabota': '', 'hh': '', 'work_city': ''}


class City(models.Model):
	name = models.CharField(max_length=64, unique=True, verbose_name='Название населенного пункта')
	slug = models.CharField(max_length=64, blank=True, unique=True)

	class Meta:
		verbose_name = 'название населенного пункта'
		verbose_name_plural = 'Названия населенных пунктов'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = from_cyrillic_to_eng(str(self.name))
		super().save(*args, **kwargs)


class Language(models.Model):
	name = models.CharField(max_length=64, unique=True, verbose_name='Язык программирования')
	slug = models.CharField(max_length=64, blank=True, unique=True)

	class Meta:
		verbose_name = 'язык программирования'
		verbose_name_plural = 'Языки программирования'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = from_cyrillic_to_eng(str(self.name))
		super().save(*args, **kwargs)


class Vacancy(models.Model):
	url = models.URLField(unique=True)
	title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
	company = models.CharField(max_length=250, verbose_name='Компания')
	description = models.TextField(verbose_name='Описание вакансии')
	city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
	language = models.ForeignKey('Language', on_delete=models.CASCADE,
	                             verbose_name='Язык программирования')
	timestamp = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name = 'вакансию'
		verbose_name_plural = 'Вакансии'
		ordering = ['-timestamp']

	def __str__(self):
		return self.title


class Error(models.Model):
	timestamp = models.DateField(auto_now_add=True)
	data = jsonfield.JSONField()

	class Meta:
		verbose_name = 'ошибку'
		verbose_name_plural = 'Ошибки'


class Urls(models.Model):
	city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
	language = models.ForeignKey('Language', on_delete=models.CASCADE,
	                             verbose_name='Язык программирования')
	url_data = jsonfield.JSONField(default=default_urls)

	class Meta:
		verbose_name = 'url'
		verbose_name_plural = "Urls"
		unique_together = ('city', 'language')
