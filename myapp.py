
from flask import Flask, render_template, request, redirect, url_for, make_response
import os, math, io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    trays = int(request.form.get("trays", 3))
    family = int(request.form.get("family", 4))
    crop = request.form.get("crop", "Collard Greens")
    season = request.form.get("season", "Summer")
    sunlight = request.form.get("sunlight", "S")
    power_mode = request.form.get("power_mode", "realistic")

    crop_yields = {
        "Collard Greens": 1.05, "Romaine Lettuce": 1.1,
        "Butterhead Lettuce": 1.0, "Kale": 1.2,
        "Spinach": 1.3, "Mustard Greens": 1.25
    }
    crop_prices = {
        "Collard Greens": 2.49, "Romaine Lettuce": 2.39,
        "Butterhead Lettuce": 2.79, "Kale": 2.69,
        "Spinach": 3.10, "Mustard Greens": 2.55
    }

    # Lighting factor based on sunlight direction and season
    season_multipliers = {"Spring": 0.9, "Summer": 0.7, "Fall": 0.85, "Winter": 1.0}
    sunlight_factors = {"N": 1.0, "NE": 0.9, "E": 0.8, "SE": 0.7, "S": 0.6,
                        "SW": 0.65, "W": 0.8, "NW": 0.9}
    base_led_usage = 35 if power_mode == "realistic" else 60
    led_wattage = trays * base_led_usage * season_multipliers.get(season, 1) * sunlight_factors.get(sunlight, 1)

    # Final values
    kwh_monthly = round((led_wattage / 1000) * 16 * 30 + 7.5, 2)
    electricity = round(kwh_monthly * 0.161, 2)
    nutrients = 10.0
    yield_rate = crop_yields[crop]
    total_yield = round(trays * 2.8 * yield_rate, 2)
    cost_per_lb = round((electricity + nutrients) / total_yield, 2) if total_yield else 0

    # Compare to store
    store_prices = {
        "Safeway": 2.49,
        "Whole Foods": 3.25,
        "Farmers Market": 2.25,
        "GrowHome": cost_per_lb
    }

    assumed_cost = trays * 50 + 100
    savings = crop_prices[crop] * total_yield - electricity - nutrients
    breakeven = math.ceil(assumed_cost / savings) if savings > 0 else None

    return render_template("index.html",
        trays=trays, family=family, crop=crop,
        season=season, sunlight=sunlight, power_mode=power_mode,
        total_yield=total_yield, electricity=electricity,
        nutrients=nutrients, cost_per_lb=cost_per_lb,
        store_prices=store_prices, assumed_cost=assumed_cost, breakeven=breakeven
    )

@app.route("/design", methods=["GET", "POST"])
def design():
    racks = int(request.form.get("racks", 2))
    trays_per_rack = int(request.form.get("trays_per_rack", 2))
    light_quality = request.form.get("light_quality", "mid")
    pump_quality = request.form.get("pump_quality", "mid")
    sensors = request.form.get("sensors") == "on"

    light_cost_map = {"low": 60, "mid": 90, "high": 150}
    pump_cost_map = {"low": 40, "mid": 70, "high": 100}
    light_cost = light_cost_map[light_quality] * racks
    pump_cost = pump_cost_map[pump_quality]
    fixed_cost = 75
    sensor_cost = 75 if sensors else 0

    build_cost = light_cost + pump_cost + fixed_cost + sensor_cost

    return render_template("design.html",
        racks=racks, trays_per_rack=trays_per_rack, light_quality=light_quality,
        pump_quality=pump_quality, sensors=sensors,
        light_cost=light_cost, pump_cost=pump_cost, fixed_cost=fixed_cost,
        build_cost=build_cost
    )

@app.route("/compare-breakeven")
def compare_breakeven():
    trays = 3
    sqft_per_tray = 2.8
    crop_prices = {"Collard Greens": 2.49, "Romaine Lettuce": 2.39, "Butterhead Lettuce": 2.79,
                   "Kale": 2.69, "Spinach": 3.10, "Mustard Greens": 2.55}
    yield_map = {"Collard Greens": 1.05, "Romaine Lettuce": 1.1, "Butterhead Lettuce": 1.0,
                 "Kale": 1.2, "Spinach": 1.3, "Mustard Greens": 1.25}

    nutrients = 10.0
    electricity = 6.0
    assumed_cost = 375

    results = []
    for crop, yield_rate in yield_map.items():
        yield_month = yield_rate * trays * sqft_per_tray
        monthly_savings = (crop_prices[crop] * yield_month) - nutrients - electricity
        breakeven = round(assumed_cost / monthly_savings) if monthly_savings > 0 else None
        results.append(breakeven if breakeven else 0)

    return render_template("compare-breakeven.html", labels=list(yield_map.keys()), data=results)

@app.route("/setup")
def setup(): return render_template("setup.html")

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    submitted = False
    if request.method == "POST":
        ease = request.form.get("ease")
        investment = request.form.get("investment")
        comments = request.form.get("comments")
        submitted = True
    return render_template("feedback.html", submitted=submitted)

@app.route("/pdf")
def pdf_export():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "GrowHome Calc Summary")
    p.drawString(100, 735, "This PDF is a placeholder for detailed system export.")
    p.save()
    buffer.seek(0)
    return make_response(buffer.read(), {
        "Content-Type": "application/pdf",
        "Content-Disposition": "attachment; filename=summary.pdf"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

@app.route("/calculations")
def calculations():
    return render_template("calculations.html")