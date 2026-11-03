import json
import re
from datetime import datetime
import os
##files = os.listdir("articles")
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "some long random secret key"
def load_articles():
    articles = []
    files = os.listdir("articles")
    for filename in files:
        with open(f"articles/{filename}", "r") as file:
            article = json.load(file)
            articles.append(article)
    return articles
def load_article_id():
    try:
        with open("article_id.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
def save_article_id(article_id):
    with open("article_id.json", "w") as file:
        json.dump(article_id, file, indent=4)
def save_article(article_id, new_article):
    with open(f"articles/article{article_id}.json", "w") as file:
        json.dump(new_article, file, indent=4)

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
            delete_id = request.form.get("id")
            try:
                os.remove(f"articles/article{delete_id}.json")
            except FileNotFoundError:
                articles = load_articles()
                error = "no such file to delete"
                return render_template("admin.html", articles=articles, error=error)
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
            date = file["date"]
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
            date = file["date"]
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
            save_article(article_id, new_article)
            return redirect(url_for("admin"))
    return render_template("edit.html", content=content, title=title, date=date)
@app.route("/save", methods=["GET", "POST"])
def save_page():
    if session.get("username") != "admin":
        return redirect(url_for("home"))
    article_id = load_article_id()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "save":
            if article_id is None:
                article_id = 1
            else:
                article_id += 1
            content = request.form.get("content")
            title = request.form.get("title")
            if content.strip() == "" or title.strip() == "":
                error = "Fields title and content should not be empty"
                return render_template("save_article.html", error=error)
            if len(content) > 5000 or len(title) > 100:
                error = "content no more than 5000 characters and title no more than a 100"
                return render_template("save_article.html", error=error, content=content, title=title)
            date = datetime.now().strftime("%Y-%m-%d")
            new_article = {"id": article_id, "content": content, "title": title, "date": date}
            save_article(article_id, new_article)
            save_article_id(article_id)
            return redirect(url_for("admin"))

        if action == "return":
            return redirect(url_for("admin"))

    return render_template("save_article.html")
app.run(debug=True)