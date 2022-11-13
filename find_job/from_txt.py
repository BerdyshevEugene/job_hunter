import csv, sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("CREATE TABLE scraping_vacancy (id, title, url, description, company, city_id, specialization_id, timestamp);")


with open('work.csv','r') as fin:
    # csv.DictReader по умолчанию использует первую строку под заголовки столбцов
    dr = csv.DictReader(fin, delimiter=";")
    to_db = [(i['title'], i['url'], i['description'], i['company'], i['city_id'], i['specialization_id']) for i in dr]

cur.executemany("INSERT INTO scraping_vacancy (title, url, description, company, city_id, specialization_id) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()