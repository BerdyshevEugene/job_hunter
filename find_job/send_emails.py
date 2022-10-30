import datetime
import django
import os, sys

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'find_job.settings'

django.setup()
from find_job.settings import (EMAIL_HOST_USER,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD
)
from scraping.models import Vacancy, Error, Url


today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий {today}'
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'

User = get_user_model()

qs = User.objects.filter(send_email=True).values(
    'city',
    'specialization',
    'email'
)
users_dict = {}

for _ in qs:
    users_dict.setdefault((_['city'], _['specialization']), [])
    users_dict[(_['city'], _['specialization'])].append(_['email'])

if users_dict:
    params = {'city_id__in': [], 'specialization_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['specialization_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params).values()[:10]
    vacancies = {}
    for _ in qs:
        vacancies.setdefault((_['city_id'], _['specialization_id']), [])
        vacancies[(_['city_id'], _['specialization_id'])].append(_)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(_html, "text/html")
            msg.send()
