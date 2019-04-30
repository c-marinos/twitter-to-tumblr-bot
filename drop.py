import sqlite3

db_file = 'connect.db'

conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute('''DROP TABLE tweets''')
conn.commit()
conn.close()
