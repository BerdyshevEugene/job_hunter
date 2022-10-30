import asyncio
import datetime as dt
import codecs
import os, sys


from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'find_job.settings'

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (work_hh, 'work_hh'),
    (work_habr, 'work_habr'),
)
jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['specialization_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['specialization_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['specialization'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, specialization = value
    job, err = await loop.run_in_executor(None, func, url, city, specialization)
    errors.extend(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['specialization'])
             for data in url_list
             for func, key in parsers]

if tmp_tasks:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    vcns = Vacancy(**job)
    try:
        vcns.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()

w = codecs.open('work.txt', 'w', 'utf-8')
w.write(str(jobs))
w.close()

ten_days_ago = dt.date.today() - dt.timedelta(30)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
