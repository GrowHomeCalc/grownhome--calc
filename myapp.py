
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        family_size = int(request.form.get('family_size', 4))
        trays = int(request.form.get('trays', 3))
        crop_type = request.form.get('crop_type', 'Collard Greens')
        season = request.form.get('season', 'Summer')
        sunlight = request.form.get('sunlight', 'S')
        lighting = request.form.get('lighting', 'Realistic Estimate')

        yield_per_tray = 2.94  # Example static value
        total_yield = trays * yield_per_tray

        electricity_cost = 4.62
        nutrient_cost = 10.00
        cost_per_lb = round((electricity_cost + nutrient_cost) / total_yield, 2)
        breakeven_months = round(250 / (total_yield * (2.49 - cost_per_lb)), 0)

        result = {
            'yield': round(total_yield, 2),
            'electricity_cost': electricity_cost,
            'nutrient_cost': nutrient_cost,
            'cost_per_lb': cost_per_lb,
            'breakeven_months': breakeven_months
        }

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/compare-breakeven')
def compare_breakeven():
    return render_template('compare-breakeven.html')

@app.route('/calculations')
def calculations():
    return render_template('calculations.html')

if __name__ == "__main__":
    app.run(debug=True)
