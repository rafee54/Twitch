import sqlite3
conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

while True:
    q = input('enter q')
    if q == 'stop':
        break;
    a = input('enter a')
    b = input('enter b')
    c.execute('INSERT INTO questions(question,a,b) VALUES(?,?,?)', (q,a,b))
    conn.commit()
    c.execute('SELECT * FROM questions ORDER BY id DESC LIMIT 1')
    print(c.fetchone())
conn.close()
