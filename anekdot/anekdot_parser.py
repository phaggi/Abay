import requests, bs4
import sqlite3
import re
import time

connection = sqlite3.connect('anecdote.db')
cursor = connection.cursor()
cursor.executescript("""create table anekdot(
        id int auto_increment primary key, anekdot longtext
    );""")
z = 0
for _ in range(3000):
    z = z + 1
    s = requests.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        reg = re.compile('[^a-zA-Zа-яА-я0-9 .,!]')
        s = reg.sub('', s)
        cursor.execute("INSERT INTO anekdot (anekdot) VALUES ('" + s + "')")
        connection.commit()
    print(z)
connection.close()
