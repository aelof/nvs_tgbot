import sqlite3

conn = sqlite3.connect('Users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE ON CONFLICT IGNORE, firstname TEXT, username TEXT, date INTEGER, phone INTEGER UNIQUE ON CONFLICT IGNORE, response STRING)''')
conn.commit()
conn.close()