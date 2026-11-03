from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        command = request.form["command"]
        x = int(request.form["x"])
        y = int(request.form["y"])
        if command == "add":
            result = x + y
        elif command == "multiply":
            result = x * y
        elif command == "substract":
            result = x - y
        elif command == "divide":
            result = x / y
    return render_template("calculator.html", result=result)
app.run(debug=True)
