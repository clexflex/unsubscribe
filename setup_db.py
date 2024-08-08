import sqlite3

conn = sqlite3.connect('unsubscribe.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS unsubscribed_emails (
    email TEXT PRIMARY KEY, 
    unsubscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()