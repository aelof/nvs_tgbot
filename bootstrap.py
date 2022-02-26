import sqlite3

conn = sqlite3.connect('Users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE ON CONFLICT IGNORE, firstname TEXT, username TEXT, name STRING, phone INTEGER UNIQUE ON CONFLICT IGNORE, response STRING, reg_date INTEGER)''')
conn.commit()
conn.close()


