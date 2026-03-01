import sqlite3

conn = sqlite3.connect('data/edge.db')
c = conn.cursor()
c.execute('SELECT * FROM edge_frames LIMIT 5')
rows = c.fetchall()
print('Total rows in DB:', len(rows))
for r in rows:
    print(r)
conn.close()
