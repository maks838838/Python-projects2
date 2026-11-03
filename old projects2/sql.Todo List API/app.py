import secrets
from datetime import datetime
import re
import bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)
def get_db():
    connection = sqlite3.connect("todolist.db")
    connection.row_factory = sqlite3.Row
    return connection
def create_token():
    return secrets.token_urlsafe(32)

def check_input(value, field):
    if not value:
        return False, f"{field} cannot be empty."
    if len(value) < 4:
        return False, f"{field} cannot be shorter than 4 characters."
    if not re.fullmatch(r"\w+", value):
        return False, f"{field} only uses characters a-z, A-Z, 0-9, and _ ."
    return True, "" 

@app.route("/todos", methods=["POST"])
@limiter.limit("9000 per minute")
def create_todo():
    db = get_db()
    data = request.get_json()

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "token is required"}), 401
    if not data:
        return jsonify({"error": "Title, description are required"}), 400
    if (data.get("title") is None or
        data.get("description") is None or
        data.get("title") == "" or
        data.get("description") == ""):
        return jsonify({"error": "Title, description are required"}), 400
    user = db.execute("""
            SELECT * FROM tokens
            WHERE token=?
        """, (token,)).fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    if user["expires_at"] != datetime.now().date().isoformat():
        return jsonify({"error": "token is not valid"}), 400
    title = data["title"]
    description = data["description"]
    user_id = user["user_id"] 
    cursor = db.execute("""
        INSERT INTO todolist
        (title, description, user_id)
        VALUES (?, ?, ?)
    """, (
        title,
        description,
        user_id,
    ))
    db.commit()
    post_id = cursor.lastrowid
    db.close()
    return jsonify({
        "id": post_id,
        "title": title,
        "description": description,
    }), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
@limiter.limit("9000 per minute")
def update_todo(todo_id):
    db = get_db()
    data = request.get_json()
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "token is required"}), 401
    if not data:
        return jsonify({"error": "Title and description are required"}), 400
    user = db.execute("""
            SELECT * FROM tokens
            WHERE token=?
        """, (token,)).fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    if user["expires_at"] != datetime.now().date().isoformat():
        return jsonify({"error": "token is not valid"}), 400
    todos = db.execute(
        "SELECT * FROM todolist WHERE id = ? and user_id=?", (todo_id, user["user_id"],)
    ).fetchall()
    if not todos:
        return jsonify({"error": "Todo not found"}), 403

    if (data.get("title") is None or
        data.get("description") is None or
        data.get("title") == "" or
        data.get("description") == ""):
        return jsonify({"error": "Title and description are required"}), 400

    title = data["title"]
    description = data["description"]

    db.execute("""
        UPDATE todolist
        SET title = ?, description = ?
        WHERE id = ?
    """, (
        title,
        description,
        todo_id
    ))
    db.commit()
    db.close()
    return jsonify({
        "id": todo_id,
        "title": title,
        "description": description
    }), 200

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
@limiter.limit("9000 per minute")
def delete_todo(todo_id):
    db = get_db()
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "token is required"}), 401
    user = db.execute("""
            SELECT * FROM tokens
            WHERE token=?
        """, (token,)).fetchone()
    if not user:
        return jsonify({"error": "Invalid token"}), 401
    if user["expires_at"] != datetime.now().date().isoformat():
        return jsonify({"error": "token is not valid"}), 400
    todos = db.execute(
        "SELECT * FROM todolist WHERE id = ? and user_id=?", (todo_id, user["user_id"],)
    ).fetchall()
    if not todos:
        return jsonify({"error": "Todo not found"}), 404
    db.execute(
        "DELETE FROM todolist WHERE id = ?",
        (todo_id,)
    )
    db.commit()
    db.close()
    return "", 204

@app.route("/todos", methods=["GET"])
@limiter.limit("9000 per minute")
def get_todos():
    db = get_db()

    token = request.headers.get("Authorization")

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    if not token:
        return jsonify({"error": "token is required"}), 401

    if page < 1 or limit < 1:
        return jsonify({"error": "page and limit must be positive"}), 400

    user = db.execute("""
        SELECT * FROM tokens
        WHERE token=?
    """, (token,)).fetchone()

    if not user:
        return jsonify({"error": "Invalid token"}), 401

    if user["expires_at"] != datetime.now().date().isoformat():
        return jsonify({"error": "token is not valid"}), 400

    term = request.args.get("term")

    offset = (page - 1) * limit

    if term:
        total = db.execute("""
            SELECT COUNT(*) FROM todolist
            WHERE user_id = ?
            AND (title LIKE ? OR description LIKE ?)
        """, (
            user["user_id"],
            f"%{term}%",
            f"%{term}%"
        )).fetchone()[0]

        todos = db.execute("""
            SELECT * FROM todolist
            WHERE user_id = ?
            AND (title LIKE ? OR description LIKE ?)
            LIMIT ? OFFSET ?
        """, (
            user["user_id"],
            f"%{term}%",
            f"%{term}%",
            limit,
            offset
        )).fetchall()

    else:
        total = db.execute("""
            SELECT COUNT(*) FROM todolist
            WHERE user_id = ?
        """, (user["user_id"],)).fetchone()[0]

        todos = db.execute("""
            SELECT * FROM todolist
            WHERE user_id = ?
            LIMIT ? OFFSET ?
        """, (
            user["user_id"],
            limit,
            offset
        )).fetchall()

    db.close()

    return jsonify({
        "data": [dict(todo) for todo in todos],
        "page": page,
        "limit": limit,
        "total": total
    }), 200
@app.route("/register", methods=["POST"])
@limiter.limit("9000 per minute")
def create_user():
    db = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "email password and login are required"}), 400
    emails = db.execute("""
            SELECT * FROM users
            WHERE email=?
        """,(data.get("email"),)).fetchall()
    if emails:
        return jsonify({"error": "email is used"}), 400
    if (data.get("email") is None or
        data.get("password") is None or
        data.get("login") is None or
        data.get("email") == "" or
        data.get("password") == "" or
        data.get("login") == ""): 
        return jsonify({"error": "email, password, login are required"}), 400
    email = data["email"]
    password = data["password"]
    login = data["login"] 
    password_ok, error = check_input(password, "password")
    if not password_ok:
        return jsonify({"error": error}), 400
    login_ok, error = check_input(login, "login")
    if not login_ok:
        return jsonify({"error": error}), 400
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) 
    hashed_password = hashed_password.decode("utf-8")
    cursor = db.execute("""
        INSERT INTO users
        (email, password, login)
        VALUES (?, ?, ?)
    """, (
        email,
        hashed_password,
        login,
    ))
    user_id = cursor.lastrowid
    token = create_token()
    expires_at = datetime.now().date().isoformat()
    db.execute("""
        INSERT INTO tokens
        (token, user_id, expires_at)
        VALUES (?, ?, ?)
    """, (
        token,
        user_id,
        expires_at,
    ))
    db.commit()
    db.close()
    return jsonify({
        "id": user_id,
        "login": login,
        "token": token,
    }), 201

@app.route("/login", methods=["POST"])
@limiter.limit("9000 per minute")
def login_user():
    db = get_db()
    data = request.get_json()
    if not data:
        return jsonify({"error": "email password and login are required"}), 400
    user = db.execute("""
            SELECT * FROM users
            WHERE email=?
        """,(data.get("email"),)).fetchone()
    if not user:
        return jsonify({"error": "we do not know that email"}), 400
    login = user["login"]
    user_id = user["id"]
    stored_hash = user["password"]
    password = data.get("password")
    if not password:
        return jsonify({"error": "password is required"}), 400
    password_ok = bcrypt.checkpw(
    password.encode("utf-8"),
    stored_hash.encode("utf-8"))
    if not password_ok:
        return jsonify({"error": "password in wrong"}), 401
    token = create_token()
    expires_at = datetime.now().date().isoformat()
    db.execute("""
        INSERT INTO tokens
        (token, user_id, expires_at)
        VALUES (?, ?, ?)
    """, (
        token,
        user_id,
        expires_at,
    ))
    db.commit()
    db.close()
    return jsonify({
        "login": login,
        "token": token,
    }), 201