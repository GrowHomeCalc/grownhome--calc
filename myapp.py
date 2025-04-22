from flask import Flask, render_template, request
import math
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    form = request.form if request.method == "POST" else {}
    trays = int(form.get("trays", 3))
    crop = form.get("crop", "Collard Greens")
    yield_rate = 1.05 if crop == "Collard Greens" else 1.0
    total_yield = trays * 2.8 * yield_rate
    electricity_cost = 6.00
    nutrients_cost = 10
    cost_per_lb = round((electricity_cost + nutrients_cost) / total_yield, 2)
    price_per_lb = 2.49
    monthly_savings = price_per_lb * total_yield - (electricity_cost + nutrients_cost)
    breakeven = math.ceil(500 / monthly_savings) if monthly_savings > 0 else None

    return f"""
    <h2>GrowHome Calc Results</h2>
    <ul>
        <li><strong>Total Yield:</strong> {round(total_yield, 2)} lbs</li>
        <li><strong>Monthly Electricity Cost:</strong> ${round(electricity_cost, 2)}</li>
        <li><strong>Estimated Cost per Pound:</strong> ${cost_per_lb}</li>
        <li><strong>Breakeven Time:</strong> {breakeven} months</li>
    </ul>
    <a href='/'>Back</a>
    """

# ✅ Port binding for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

