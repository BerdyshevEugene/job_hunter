from sqlite3 import Timestamp
from django.db import models

from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {'work_habr': ''}


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Specialization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'specialization'
        verbose_name_plural = 'specializations'

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
    city = models.ForeignKey(
        'City',
        on_delete = models.CASCADE,
        verbose_name = 'Город'
    )
    specialization = models.ForeignKey(
        'Specialization',
        on_delete = models.CASCADE,
        verbose_name = 'Язык программирования'
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'vacancy'
        verbose_name_plural = 'vacancies'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey(
        'City',
        on_delete = models.CASCADE,
        verbose_name = 'city'
    )
    specialization = models.ForeignKey(
        'Specialization',
        on_delete = models.CASCADE,
        verbose_name = 'specialization'
    )
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'specialization')
