from email import header
import requests
import codecs  # для расшифровки получаемых данных

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

url = 'https://spb.hh.ru/vacancies/programmist_python'
resp = requests.get(url, headers=headers)

w = codecs.open('work.html', 'w', 'utf-8')
w.write(str(resp.text))
w.close()