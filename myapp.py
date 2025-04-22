
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Safe parsing of inputs
        try:
            trays = int(request.form.get('trays', 2))
            family_size = int(request.form.get('family_size', 4))
            crop_type = request.form.get('crop_type', 'Collard Greens')
            season = request.form.get('season', 'Summer')
            sunlight = request.form.get('sunlight', 'S')
            lighting = request.form.get('lighting', 'Realistic Estimate')

            yield_map = {
                "Collard Greens": 2.94,
                "Romaine Lettuce": 2.75,
                "Butterhead Lettuce": 2.4,
                "Spinach": 2.1,
                "Kale": 2.6,
                "Mustard Greens": 2.9
            }
            seasonal_factor = {
                "Winter": 0.75,
                "Spring": 1.0,
                "Summer": 1.2,
                "Fall": 0.9
            }

            yield_rate = yield_map.get(crop_type, 2.5)
            season_mult = seasonal_factor.get(season, 1.0)

            yield_month = trays * yield_rate * season_mult
            electricity_cost = trays * 1.54
            nutrient_cost = trays * 3.33
            total_cost = electricity_cost + nutrient_cost
            cost_per_pound = round(total_cost / yield_month, 2) if yield_month > 0 else 0
            assumed_cost = 250
            monthly_savings = (2.49 * yield_month) - total_cost
            breakeven_months = round(assumed_cost / monthly_savings, 1) if monthly_savings > 0 else "N/A"

            result = {
                'yield_month': round(yield_month, 2),
                'electricity_cost': round(electricity_cost, 2),
                'nutrient_cost': round(nutrient_cost, 2),
                'cost_per_pound': cost_per_pound,
                'breakeven_months': breakeven_months
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/setup')
def setup():
    return render_template("setup.html")

@app.route('/design')
def design():
    return render_template("design.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

@app.route('/compare-breakeven')
def compare_breakeven():
    return render_template("compare-breakeven.html")

@app.route('/calculations')
def calculations():
    return render_template("calculations.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
