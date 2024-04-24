"""
Distributed Systems Project
24.04.2024

Sources used for creation of code:

Distributed Systems Assignment 4 was used as inspiration

https://www.youtube.com/watch?v=3UOyky9sEQY This video helped in learning the basics
https://docs.python.org/3.9/library/socket.html Helped to understand python socket protocols as a whole
https://docs.python.org/3.9/library/threading.html Helped to understand python threading protocols
https://realpython.com/python-sockets/#socket-api-overview Helped to understand socket communication
"""

import sqlite3

### Connect to db (sql3)
conn = sqlite3.connect('chat.db')

cursor = conn.cursor()

### Create table to store user information for authentication
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL
                )''')

# Create a table to store messages
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    recipient TEXT,
                    message TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    private BOOLEAN DEFAULT FALSE
                )''')

# Commit & Close
conn.commit()
conn.close()