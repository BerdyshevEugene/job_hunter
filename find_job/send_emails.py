import datetime
import django
import os, sys

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'find_job.settings'

django.setup()
from scraping.models import Vacancy, Error, Url
from find_job.settings import (EMAIL_HOST_USER,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD
)

ADMIN_USER = EMAIL_HOST_USER


today = datetime.date.today()
subject = f'Рассылка вакансий за {today}'
text_content = f'Рассылка вакансий {today}'
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению, на сегодня, по интересующим вас вакансиям данных нет.</h2>'

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
    # qs = Vacancy.objects.filter(**params, timestamp=today).values()
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

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
    subject += f'Ошибки парсинга {today}'
    text_content += 'Ошибки парсинга'
    data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей </h2>'
        for i in data:
            _html += f'<p">Город: {i["city"]}, Специальность:{i["specialization"]}, email:{i["email"]}</p><br>'
        subject += f'Пожелания пользователей {today}'
        text_content += 'Пожелания пользователей'

qs = Url.objects.all().values('city', 'specialization')
urls_dict = {(i['city'], i['specialization']): True for i in qs}
urls_err = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        if keys[0] and keys[1]:
            urls_err += f'<p"> Для города: {keys[0]} и ЯП: {keys[1]} отсутствуют urls</p><br>'
if urls_err:
    subject += 'Отсутствующие urls'
    _html += '<hr>'
    _html += '<h2>Отсутствующие urls</h2>'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, 'text/html')
    msg.send()
