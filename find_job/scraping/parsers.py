import requests
import codecs  # для расшифровки получаемых данных
from bs4 import BeautifulSoup as BS
from random import randint


__all__ = ('work_habr') # для импорта функций из файла

headers = [
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16;'
        'rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


# def work_hh(url, city=None, specialization=None):
#     jobs = []
#     errors = []
#     domain = 'https://hh.ru'
#     if url:
#         resp = requests.get(url, headers[randint(0, 5)])
#         if resp.status_code == 200:
#             soup = BS(resp.content, 'html.parser')
#             main_div = soup.find('div', id = 'a11y-main-content')
#             if main_div:
#                 div_roster = main_div.find_all(
#                     'div', attrs={'class': 'vacancy-serp-item__layout'}
#                 )
#                 for div in div_roster:
#                     title = div.find('h3')
#                     href = title.a['href']
#                     try:
#                         description = div.find(
#                             'div',
#                             attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_'
#                                     'responsibility'}
#                         ).text
#                         requirements = div.find(
#                             'div',
#                             attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_'
#                             'requirement'}
#                         ).text
#                     except:
#                         description = 'None'
#                         requirements = 'None'
#                     try:
#                         company = div.find(
#                             'a', attrs = {'data-qa': 'vacancy-serp__vacancy-employer'}
#                         ).text
#                     except:
#                         company = 'None'
#                     jobs.append(
#                         {'title': title.text, 'url': href, 'description': description +
#                         '' + requirements, 'company': company, 'city_id': city,
#                         'specialization_id': specialization}
#                     )
#             else:
#                 errors.append({'url': url, 'title': 'div does not exists'})
#         else:
#             errors.append({'url': url, 'title': 'Page not responding'})
#     print(jobs, errors)
#     return jobs, errors


def work_habr(url, city=None, specialization=None):
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
    if url:
        resp = requests.get(url, headers[randint(0, 5)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find(
                'div',
                attrs = {'class':'content-wrapper__main content-wrapper__main--left'}
            )
            if main_div:
                div_roster = main_div.find_all(
                    'div', attrs = {'class': 'vacancy-card'}
                )
                for div in div_roster:
                    title = div.find(
                        'div',
                        {'class': 'vacancy-card__title'}
                    ).find('a').text
                    href = div.find(
                        'div',
                        {'class': 'vacancy-card__title'}
                    ).find('a').get('href')
                    hrefs = []
                    hrefs.append('https://career.habr.com' + href)
                    for link in hrefs:
                        response = requests.get(link, headers[randint(0, 2)])
                        soup = BS(response.text, 'html.parser')
                        if resp.status_code == 200:
                            try:
                                description = soup.find(
                                    'div',
                                    {'class': "style-ugc"}
                                ).text
                            except:
                                description = 'None'
                        else:
                            errors.append(
                                {'url': link,
                                'title': 'Page not responding'}
                            )
                    try:
                        company = div.find(
                            'div',
                            attrs = {'class': 'vacancy-card__company-title'}
                        ).text
                    except:
                        company = 'None'
                    try:
                        city = div.find(
                            'div',
                            attrs = {'class': 'vacancy-card__meta'}
                        ).find('a').text
                    except:
                        city = 'None'
                    # try:
                    #     specialization = div.find('div', attrs = {'class': 'link-comp link-comp--appearance-dark'}).find('a').text
                    # except:
                    #     specialization = 'None'
                    jobs.append(
                        {'title': title, 'url': domain + href,
                        'description': description, 'company': company,
                        'city_id': city, 'specialization_id': specialization}
                    )
            else:
                errors.append({'url': url, 'title': 'div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page not responding'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://career.habr.com/vacancies?q=python&l=1&type=all'
    jobs, errors = work_habr(url)
    w = codecs.open('work.csv', 'w', 'utf-8')
    w.write(str(jobs))
    w.close()
