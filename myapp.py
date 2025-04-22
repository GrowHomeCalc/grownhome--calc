
from flask import Flask, render_template, request, redirect, url_for
import math, os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    trays = int(request.form.get("trays", 3)) if request.method == "POST" else 3
    family = int(request.form.get("family", 4)) if request.method == "POST" else 4
    crop = request.form.get("crop", "Collard Greens") if request.method == "POST" else "Collard Greens"

    crop_yields = {
        "Collard Greens": 1.05,
        "Romaine Lettuce": 1.1,
        "Butterhead Lettuce": 1.0,
        "Kale": 1.2,
        "Spinach": 1.3,
        "Mustard Greens": 1.25
    }

    price_per_lb = {
        "Collard Greens": 2.49,
        "Romaine Lettuce": 2.39,
        "Butterhead Lettuce": 2.79,
        "Kale": 2.69,
        "Spinach": 3.10,
        "Mustard Greens": 2.55
    }

    yield_rate = crop_yields[crop]
    market_price = price_per_lb[crop]
    yield_per_tray = 2.8 * yield_rate
    total_yield = trays * yield_per_tray
    electricity_cost = 6.0
    nutrients_cost = 10.0
    total_cost = electricity_cost + nutrients_cost
    cost_per_lb = round(total_cost / total_yield, 2)
    monthly_savings = market_price * total_yield - total_cost
    assumed_cost = trays * 50 + 90  # Simulated cost logic
    breakeven = math.ceil(assumed_cost / monthly_savings) if monthly_savings > 0 else None

    return render_template("index.html",
        trays=trays,
        family=family,
        crop=crop,
        total_yield=round(total_yield, 2),
        electricity=round(electricity_cost, 2),
        nutrients=round(nutrients_cost, 2),
        cost_per_lb=cost_per_lb,
        breakeven=breakeven,
        assumed_cost=assumed_cost
    )

@app.route("/design")
def design():
    return render_template("design.html")

@app.route("/setup")
def setup():
    return render_template("setup.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/compare-breakeven")
def compare_breakeven():
    return render_template("compare-breakeven.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
