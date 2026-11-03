import sqlite3

connection = sqlite3.connect("todolist.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

connection.execute("""
    CREATE TABLE IF NOT EXISTS expences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        expence TEXT NOT NULL,
        categorie TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")


connection.commit()
connection.close()