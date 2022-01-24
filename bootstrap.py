import sqlite3

conn = sqlite3.connect('Users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users  (id integer primary key, user_id integer, user_name text, user_surname text, username text)''')
conn.commit()
conn.close()