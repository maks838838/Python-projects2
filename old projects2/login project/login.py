import re
import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
def check_input(value, field):
    if not value:
        return False, f"{field} cannot be empty."
    if value is None:
        return False, f"{field} cannot be empty."
    if len(value) < 6:
        return False, f"{field} cannot be shorter than 6 characters."
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
@app.route("/", methods=["GET", "POST"])
def main():
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
                return render_template("index.html", error=error)
            password_ok, error = check_input(password, "password")
            if not password_ok:
                return render_template("index.html", error=error)
            used=False
            for user in user_list:
                if user["login"] == login:
                    used=True
                    break
            if used:
                error="invalid login is used"    
                return render_template("index.html", error=error)
            if password == password_check:
                if len(user_list) == 0:
                    user_id = 1
                else:
                    user_id = user_list[-1]["id"]+1
                new_user = {"id": user_id, "login": login, "password": password}
                user_list.append(new_user)
                save_user_list(user_list)
                return redirect(url_for("main"))
            else:
                error = "passwords are not the same"
                return render_template("index.html", error=error)    
        if action == "login":
            for user in user_list:
                if user["login"] == login:
                    if user["password"] == password:
                        pass
    return render_template("index.html", error=error) 
app.run(debug=True)
