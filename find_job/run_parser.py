import asyncio
import codecs
import os, sys


from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'find_job.settings'

import django
django.setup()

from find_jobs.parser import *
from find_jobs.models import Vacancy, City, Specialization, Error, Url


User = get_user_model()

parser = (
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
        tmp = {}
        tmp['city'] = pair[0]
        tmp['specialization'] = pair[1]
        tmp['url_data'] = url_dict[pair]
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
             for func, key in parser]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

for job in jobs:
    vcns = Vacancy(**job)
    try:
        vcns.save()
    except DatabaseError:
        pass
if errors:
    errs = Error(data=errors).save()

w = codecs.open('work.txt', 'w', 'utf-8')
w.write(str(jobs))
w.close()
