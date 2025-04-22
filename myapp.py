
from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {
        'family_size': 4,
        'trays': 3,
        'crop_type': 'Collard Greens',
        'season': 'Summer',
        'sunlight': 'S',
        'lighting': 'Realistic Estimate'
    }

    if request.method == 'POST':
        form_data['family_size'] = int(request.form.get('family_size', 4))
        form_data['trays'] = int(request.form.get('trays', 3))
        form_data['crop_type'] = request.form.get('crop_type', 'Collard Greens')
        form_data['season'] = request.form.get('season', 'Summer')
        form_data['sunlight'] = request.form.get('sunlight', 'S')
        form_data['lighting'] = request.form.get('lighting', 'Realistic Estimate')

        crop_yields = {
            'Collard Greens': 2.94,
            'Romaine Lettuce': 2.75,
            'Butterhead Lettuce': 2.4,
            'Spinach': 2.1,
            'Kale': 2.6,
            'Mustard Greens': 2.9
        }
        kwh_cost = 0.15
        led_watts = 150 if form_data['lighting'] == 'Realistic Estimate' else 250
        seasonal_multipliers = {'Winter': 0.75, 'Spring': 1.0, 'Summer': 1.2, 'Fall': 0.9}
        nutrient_cost = 10

        yield_per_tray = crop_yields.get(form_data['crop_type'], 2.0)
        seasonal_multiplier = seasonal_multipliers.get(form_data['season'], 1.0)

        total_yield = form_data['trays'] * yield_per_tray * seasonal_multiplier
        monthly_energy_cost = round((led_watts * form_data['trays'] * 16 * 30 / 1000) * kwh_cost, 2)
        monthly_cost = monthly_energy_cost + nutrient_cost
        cost_per_pound = round(monthly_cost / total_yield, 2) if total_yield > 0 else 0
        breakeven_months = round(250 / monthly_cost) if monthly_cost > 0 else float('inf')

        result = {
            'total_yield': round(total_yield, 2),
            'monthly_electricity_cost': monthly_energy_cost,
            'monthly_nutrient_cost': nutrient_cost,
            'cost_per_pound': cost_per_pound,
            'breakeven_months': breakeven_months
        }

    return render_template("index.html", form=form_data, result=result)

if __name__ == '__main__':
    app.run(debug=True)
