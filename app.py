from flask import Flask, render_template, request, make_response, session
import csv, io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for sessions

@app.route('/calculations', methods=['POST'])
def calculations():
    trays = int(request.form.get('trays', 1))
    family_size = int(request.form.get('family_size', 1))
    crop_type = request.form.get('crop_type')
    season = request.form.get('season')
    sunlight_direction = request.form.get('sunlight_direction')
    lighting_mode = request.form.get('lighting_mode')
    light_type = request.form.get('light_type')
    pump_type = request.form.get('pump_type')
    sensors = request.form.get('sensors')

    tray_cost = 40
    light_costs = {'low': 50, 'mid': 100, 'high': 200}
    pump_costs = {'low': 30, 'mid': 60, 'high': 120}
    sensor_cost = 75 if sensors == 'yes' else 0

    crop_yields = {
        'lettuce': 2.5,
        'basil': 1.8,
        'kale': 2.0,
        'spinach': 2.2,
        'mustard': 2.3,
        'cilantro': 1.5,
        'parsley': 1.4,
        'thyme': 0.9,
        'mint': 1.7,
        'chives': 1.3,
        'arugula': 2.1,
        'oregano': 1.1
    }
    yield_per_tray = crop_yields.get(crop_type, 2.0)

    season_multiplier = {
        'spring': 1.0,
        'summer': 1.1,
        'fall': 0.95,
        'winter': 0.85
    }

    lighting_multiplier = 1.0 if lighting_mode == 'realistic' else 1.2
    electricity_cost_per_tray = 5 if lighting_mode == 'realistic' else 10
    nutrient_cost_per_tray = 3

    weekly_demand_lbs = family_size * 1.5
    monthly_demand_lbs = weekly_demand_lbs * 4
    recommended_trays = round(monthly_demand_lbs / (yield_per_tray * season_multiplier[season]))

    estimated_cost = (trays * tray_cost) + light_costs[light_type] + pump_costs[pump_type] + sensor_cost
    seasonal_yield = trays * yield_per_tray * season_multiplier[season]
    estimated_yield = seasonal_yield
    cost_per_pound = round(estimated_cost / (estimated_yield * 6), 2) if estimated_yield > 0 else 0
    electricity_total = trays * electricity_cost_per_tray
    nutrients_total = trays * nutrient_cost_per_tray

    market_price_per_lb = 4
    value_per_month = estimated_yield * market_price_per_lb
    breakeven_month = round(estimated_cost / value_per_month, 1) if value_per_month > 0 else 0

    session['system_cost'] = estimated_cost
    session['monthly_value'] = value_per_month

    return render_template(
        'calculations.html',
        trays=trays,
        family_size=family_size,
        crop_type=crop_type,
        season=season,
        sunlight_direction=sunlight_direction,
        lighting_mode=lighting_mode,
        estimated_cost=estimated_cost,
        estimated_yield=round(estimated_yield, 2),
        electricity_total=round(electricity_total, 2),
        nutrients_total=round(nutrients_total, 2),
        cost_per_pound=cost_per_pound,
        breakeven_month=breakeven_month,
        recommended_trays=recommended_trays
    )

if __name__ == '__main__':
    app.run(debug=True)
