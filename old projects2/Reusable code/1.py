
## Load JSON data from a file. Returns None if the file is missing or invalid.
def load_file(file_name):
    try:
        with open(f"{file_name}.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

## Save data to a JSON file.
def save_file(file_name, data):
    with open(f"{file_name}.json", "w") as file:
        json.dump(data, file, indent=4)


## function that checks values takes a name of the field as "field" and "value" as a value of an input
def check_input(value, field, min_lenght=6,):
    if value is None:
        return False, f"{field} cannot be empty."
    if len(value) < min_lenght:
        return False, f"{field} cannot be shorter than 4 characters."
    if not re.fullmatch(r"\w+", value):
        return False, f"{field} only uses characters a-z, A-Z, 0-9, and _ ."
    return True, "" 
    
def Login_code():
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