

connection = sqlite3.connect("blog.db")
connection.row_factory = sqlite3.Row

posts = connection.execute("SELECT * FROM posts").fetchall()

for post in posts:
    print(dict(post))

connection.close()