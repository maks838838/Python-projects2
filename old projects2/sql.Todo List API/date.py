from datetime import datetime, timedelta
expires_at = (datetime.now() + timedelta(days=1)).date().isoformat()
today = datetime.now().date().isoformat()
if expires_at = today:
    return 

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