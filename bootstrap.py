import sqlite3

conn = sqlite3.connect('Users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users  (id integer primary key, user_id integer, user_name text)''')
conn.commit()
conn.close()