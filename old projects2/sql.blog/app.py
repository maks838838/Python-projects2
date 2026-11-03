import sqlite3
import json
import re
from flask import jsonify
from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, session

def get_db():
    connection = sqlite3.connect("blog.db")
    connection.row_factory = sqlite3.Row
    return connection
def edit_post(article_id, title, content):
    db = get_db()

    db.execute("""
        UPDATE posts
        SET title = ?, content = ?, updated_at = ?
        WHERE id = ?
    """, (
        title,
        content,
        datetime.now().isoformat(),
        article_id
    ))
    db.commit()
    db.close()
def add_to_db(data):
    db = get_db()

    cursor = db.execute("""
        INSERT INTO posts (title, content, category, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["content"],
        data["category"],
        data["tag"],
        datetime.now().isoformat(),
        datetime.now().isoformat()
    ))

    db.commit()

    article_id = cursor.lastrowid

    db.close()

    return article_id
def delete_post(delete_id):
    db = get_db()
    db.execute(
        "DELETE FROM posts WHERE id = ?",
        (delete_id,)
    )
    db.commit()
    db.close()
app = Flask(__name__)
app.secret_key = "some long random secret key"
def load_articles():
    db = get_db()

    articles = db.execute(
        "SELECT * FROM posts"
    ).fetchall()

    db.close()

    return articles
def check_input(value, field):
    if not value:
        return False, f"{field} cannot be empty."
    if value is None:
        return False, f"{field} cannot be empty."
    if len(value) < 4:
        return False, f"{field} cannot be shorter than 4 characters."
    if not re.fullmatch(r"\w+", value):
        return False, f"{field} only uses characters a-z, A-Z, 0-9, and _ ."
    return True, "" 
def load_user_list():
    try:
        with open("user_list.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def save_user_list(user_list):
    with open("user_list.json", "w") as file:
        json.dump(user_list, file, indent=4)
@app.route("/user", methods=["GET", "POST"])        
def user():
    articles = load_articles()
    if request.method == "POST":
       action = request.form.get("action")
       if action == "logout":
            session.clear()
            return redirect(url_for("home"))
    return render_template("user.html", articles=articles)   
@app.route("/posts", methods=["POST"])
def create_post():
    db = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Title, content, category and tags are required"}), 400
    if data.get("title") is None or data.get("content") is None or data.get("category") is None or data.get("tags") is None or data.get("title") == "" or data.get("content") == "" or data.get("category") == "" or data.get("tags") == "": 
        return jsonify({"error": "Title, content, category and tags are required"}), 400
    title = data["title"]
    content = data["content"]
    category = data["category"]
    tags = data["tags"]
    time = datetime.now().isoformat()
    
    cursor = db.execute("""
        INSERT INTO posts
        (title, content, category, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        content,
        category,
        json.dumps(tags),
        time,
        time
    ))

    db.commit()

    post_id = cursor.lastrowid
    db.close()

    return jsonify({
        "id": post_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "createdAt": time,
        "updatedAt": time
    }), 201
@app.route("/posts/<int:article_id>", methods=["PUT"])
def update_post(article_id):
    db = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Title, content, category and tags are required"}), 400
    articles = db.execute(
        "SELECT * FROM posts WHERE id = ?", (article_id,)
    ).fetchall()
    if not articles :
        return jsonify({"error": "Post not found"}), 404
    if data.get("title") is None or data.get("content") is None or data.get("category") is None or data.get("tags") is None or data.get("title") == "" or data.get("content") == "" or data.get("category") == "" or data.get("tags") == "": 
        return jsonify({"error": "Title, content, category and tags are required"}), 400
    title = data["title"]
    content = data["content"]
    category = data["category"]
    tags = data["tags"]
    time = datetime.now().isoformat()
    


    
    result = db.execute("""
        UPDATE posts
        SET title = ?, content = ?, category = ?, tags = ?, updated_at = ?
        WHERE id = ?
    """, (
        title,
        content,
        category,
        json.dumps(tags),
        time,
        article_id
    ))

    db.commit()
    db.close()

    return jsonify({
        "id": article_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
        "updatedAt": time
    }), 200
@app.route("/posts/<int:article_id>", methods=["DELETE"])
def delete_post(article_id):
    db = get_db()
    
    articles = db.execute(
        "SELECT * FROM posts WHERE id = ?", (article_id,)
    ).fetchall()
    if not articles :
        return jsonify({"error": "Post not found"}), 404
    db.execute(
        "DELETE FROM posts WHERE id = ?",
        (article_id,)
    )
    db.commit()
    db.close()
    return "", 204

@app.route("/posts", methods=["GET"])
def get_posts():
    db = get_db()
    
    term = request.args.get("term")

    if term:
        articles = db.execute("""
            SELECT * FROM posts
            WHERE title LIKE ?
               OR content LIKE ?
               OR category LIKE ?
        """, (
            f"%{term}%",
            f"%{term}%",
            f"%{term}%"
        )).fetchall()
    else:
        articles = db.execute(
            "SELECT * FROM posts"
        ).fetchall()
    db.close()

    return jsonify([dict(article) for article in articles])

@app.route("/home", methods=["GET", "POST"])
def home():
    error = ""
    user_list = load_user_list()
    login = request.form.get("login")
    password = request.form.get("password")
    password_check = request.form.get("password_check")
    if request.method == "POST":
        action = request.form.get("action")
        if action == "register":
            login_ok, error = check_input(login, "login")
            if not login_ok:
                return render_template("login.html", error=error)
            password_ok, error = check_input(password, "password")
            if not password_ok:
                return render_template("login.html", error=error)
            used=False
            for user in user_list:
                if user["login"] == login:
                    used=True
                    break
            if used:
                error="invalid login is used"    
                return render_template("login.html", error=error)
            if password == password_check:
                if len(user_list) == 0:
                    user_id = 1
                else:
                    user_id = user_list[-1]["id"]+1
                new_user = {"id": user_id, "login": login, "password": password}
                user_list.append(new_user)
                save_user_list(user_list)
                return redirect(url_for("home"))
            else:
                error = "passwords are not the same"
                return render_template("login.html", error=error)    
        if action == "login":
            for user in user_list:
                if user["login"] == login:
                    if user["password"] == password:
                        if password == "admin" and login == "admin":
                            articles = load_articles()
                            session["logged_in"] = True
                            session["username"] = "admin"
                            return render_template("admin.html", articles=articles)
                        articles = load_articles()
                        session["username"] = login
                        session["logged_in"] = True
                        return render_template("user.html", articles=articles)     
            return render_template("login.html",  error="password or login is invalid")
    return render_template("login.html")
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
@app.route("/", methods=["GET", "POST"])
def admin():
    if session.get("username") != "admin":
        return redirect(url_for("home"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "delete":
            delete_id = int(request.form.get("id"))
            delete_post(delete_id)
            return redirect(url_for("admin"))
        if action == "logout":
            session.clear()
            return redirect(url_for("home"))
    articles = load_articles()
    return render_template("admin.html", articles=articles)
@app.route("/look/<int:article_id>", methods=["GET", "POST"])
def look(article_id):
    articles = load_articles()
    for file in articles:
        if file["id"] == article_id:
            title = file["title"]
            content = file["content"]
            created_at = datetime.fromisoformat(file["created_at"])
            date = created_at.strftime("%Y.%m.%d")
            return render_template("look.html", content=content, title=title, date=date)
    return render_template("404.html"), 404
@app.route("/edit/<int:article_id>", methods=["GET", "POST"])
def edit(article_id):
    if session.get("username") != "admin":
        return redirect(url_for("home"))
    articles = load_articles()
    for file in articles:
        if file["id"] == article_id:
            title = file["title"]
            content = file["content"]
            created_at = datetime.fromisoformat(file["created_at"])
            date = created_at.strftime("%Y.%m.%d")
            break
    else:
        return render_template("404.html"), 404
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save_changes":
            content = request.form.get("content")
            title = request.form.get("title")
            date = request.form.get("date")
            if content.strip() == "" or title.strip() == "":
                error = "Fields title and content should not be empty"
                return render_template("edit.html", error=error, content=content, title=title, date=date)
            if len(content) > 5000 or len(title) > 100:
                error = "content no more than 5000 characters and title no more than a 100"
                return render_template("edit.html", error=error, content=content, title=title, date=date)
            new_article = {"id": article_id, "content": content, "title": title, "date": date}
            edit_post(article_id, title, content)
            
            return redirect(url_for("admin"))
    return render_template("edit.html", content=content, title=title, date=date)
@app.route("/save", methods=["GET", "POST"])
def save_page():
    if session.get("username") != "admin":
        return redirect(url_for("home"))

    
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save":
            content = request.form.get("content")
            title = request.form.get("title")
            
            if content.strip() == "" or title.strip() == "":
                error = "Fields title and content should not be empty"
                return render_template("save_article.html", error=error)
            if len(content) > 5000 or len(title) > 100:
                error = "content no more than 5000 characters and title no more than a 100"
                return render_template("save_article.html", error=error, content=content, title=title)
            date = datetime.now().strftime("%Y-%m-%d")
            
            
            data={"category": "bad category", "content": content, "title": title, "tag": "no tag"}
            article_id = add_to_db(data)
            return redirect(url_for("admin"))
        if action == "return":
            return redirect(url_for("admin"))
    return render_template("save_article.html")

app.run(debug=True)