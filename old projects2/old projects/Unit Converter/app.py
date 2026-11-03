from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
units_of_length = {
    "millimeter": 1,
    "centimeter": 10,
    "meter": 1000,
    "kilometer": 1_000_000,
    "inch": 25.4,
    "foot": 304.8,
    "yard": 914.4,
    "mile": 1_609_344}
weight_units = {
    "milligram": 1,
    "gram": 1000,
    "kilogram": 1_000_000,
    "ounce": 28_349.5,
    "pound": 453_592}
def convert(amount, base_unit, end_unit, units):
    if amount is None or not base_unit or not end_unit:
        return None
    value1 = units[end_unit]
    value2 = units[base_unit]
    result = amount*(value2/value1)
    return result
def get_base_values():
    try:
        amount = float(request.form["amount"])
        base_unit = request.form["base_unit"]
        end_unit = request.form["end_unit"]
    except (ValueError, TypeError, KeyError):
        return None, None, None
    return amount, base_unit, end_unit
@app.route("/", methods=["GET", "POST"])
def main():
    result = 0
    result1 = 0
    result2 = 0
    if request.method == "POST":
        action = request.form.get("action")
        if action == "convert_weight":
            amount, base_unit, end_unit = get_base_values()
            result1 = convert(amount, base_unit, end_unit, weight_units)
        elif action == "convert_length":
            amount, base_unit, end_unit = get_base_values()
            result = convert(amount, base_unit, end_unit, units_of_length)
        elif action == "convert_temperature":
            amount, base_unit, end_unit = get_base_values()
            if base_unit == "°C":
                if end_unit == "°F":
                    result2 = amount * 9/5 + 32
                elif end_unit == "K":
                    result2 = amount + 273.15
                elif end_unit == "°C":
                    result2 = amount
            elif base_unit == "°F":
                if end_unit == "°C":
                    result2 = (amount - 32) * 5/9
                elif end_unit == "K":
                    result2 = (amount - 32) * 5/9 + 273.15
                elif end_unit == "°F":
                    result2 = amount
            elif base_unit == "K":
                if end_unit == "°C":
                    result2 = amount - 273.15
                elif end_unit == "°F":
                    result2 = (amount - 273.15) * 9/5 + 32
                elif end_unit == "K":
                    result2 = amount
    return render_template(
            "index.html",
            result=result, 
            result1=result1,
            result2=result2
            )
app.run(debug=True)
