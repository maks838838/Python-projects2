import requests
from datetime import datetime
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
API_KEY = "5FS37GUF93FNDVM4V94529AFY"
from flask import Flask, render_template, request, redirect, url_for, session
import redis
app = Flask(__name__)
cache = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379",
    default_limits=["100 per day", "20 per hour"]
)
@app.route("/", methods=["GET", "POST"])   
@limiter.limit("10 per minute")
def user():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "run":
            city = request.form.get("city").strip().lower()
            date1 = datetime.now().strftime("%Y-%m-%d")
            cached_data = cache.get(city)
            if cached_data:
                data = json.loads(cached_data)
            else:
                url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date1}/?key={API_KEY}"
                response = requests.get(url)
                data = response.json()
                cache.set(city, json.dumps(data), ex=43200)
            
            weather = {
                "city": data["resolvedAddress"],
                "temperature": data["currentConditions"]["temp"],
                "conditions": data["currentConditions"]["conditions"],
                "humidity": data["currentConditions"]["humidity"],
                "wind_speed": data["currentConditions"]["windspeed"],
                "pressure": data["currentConditions"]["pressure"],
                "sunrise": data["currentConditions"]["sunrise"],
                "sunset": data["currentConditions"]["sunset"]
            }
            return render_template("weather.html", weather=weather)   
    return render_template("weather.html", weather=None)
app.run(debug=True)
