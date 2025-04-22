
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form = request.form if request.method == 'POST' else {}

    if request.method == 'POST':
        try:
            trays = int(form.get('trays', 3))
            family_size = int(form.get('family_size', 4))
            crop_type = form.get('crop_type', 'Collard Greens')
            season = form.get('season', 'Summer')
            sunlight = form.get('sunlight', 'S')
            lighting_mode = form.get('lighting_mode', 'Realistic Estimate')

            # Sample calculation logic
            yield_per_tray = 2.94 if crop_type == "Collard Greens" else 2.0
            total_yield = trays * yield_per_tray
            electricity_cost = trays * 1.54
            nutrient_cost = trays * 3.33
            cost_per_pound = round((electricity_cost + nutrient_cost) / total_yield, 2)
            build_cost = 250
            months_to_break_even = round(build_cost / ((2.49 * total_yield) - (electricity_cost + nutrient_cost)), 2)

            result = {
                "total_yield": round(total_yield, 2),
                "electricity_cost": round(electricity_cost, 2),
                "nutrient_cost": round(nutrient_cost, 2),
                "cost_per_pound": cost_per_pound,
                "months_to_break_even": months_to_break_even,
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True)
