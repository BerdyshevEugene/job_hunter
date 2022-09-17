from sqlite3 import Timestamp
from django.db import models
from slugify import slugify


def default_urls():
    return {'work_hh': '', 'work_habr': ''}


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class Specialization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'specializations'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Specialization, self).save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='vacancy title')
    company = models.CharField(max_length=250, verbose_name='company')
    description = models.TextField(verbose_name='vacancy description')
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
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
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
