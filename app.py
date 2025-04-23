from flask import Flask, render_template, request, make_response, session
import csv, io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session to work

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/breakeven')
def breakeven():
    system_cost = session.get('system_cost', 500)
    monthly_value = session.get('monthly_value', 60)
    return render_template('breakeven.html', system_cost=system_cost, monthly_value=monthly_value)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user_feedback = request.form.get('feedback')
        print("Feedback received:", user_feedback)  # For now, prints to console
    return render_template('feedback.html')

@app.route('/calculations', methods=['POST'])
def calculations():
    trays = int(request.form.get('trays', 1))
    light_type = request.form.get('light_type')
    pump_type = request.form.get('pump_type')
    sensors = request.form.get('sensors')

    light_costs = {'low': 50, 'mid': 100, 'high': 200}
    pump_costs = {'low': 30, 'mid': 60, 'high': 120}
    sensor_cost = 75 if sensors == 'yes' else 0
    tray_cost = 40

    estimated_cost = (trays * tray_cost) + light_costs[light_type] + pump_costs[pump_type] + sensor_cost

    # 🌱 Yield estimate logic
    yield_per_tray = 2.5  # lbs per tray per month
    estimated_yield = trays * yield_per_tray

    # Store for breakeven chart
    session['system_cost'] = estimated_cost
    session['monthly_value'] = trays * yield_per_tray * 4  # $4/lb

    return render_template(
        'calculations.html',
        estimated_cost=estimated_cost,
        trays=trays,
        estimated_yield=estimated_yield,
        tray_cost=trays * tray_cost,
        light_cost=light_costs[light_type],
        pump_cost=pump_costs[pump_type],
        sensor_cost=sensor_cost
    )

@app.route('/download-report', methods=['POST'])
def download_report():
    trays = int(request.form.get('trays'))
    tray_cost = trays * 40
    light_cost = int(request.form.get('light_cost'))
    pump_cost = int(request.form.get('pump_cost'))
    sensor_cost = int(request.form.get('sensor_cost'))
    total_cost = tray_cost + light_cost + pump_cost + sensor_cost
    estimated_yield = trays * 2.5  # lbs per month

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Component', 'Cost (USD)'])
    writer.writerow(['Grow Trays', tray_cost])
    writer.writerow(['Lighting', light_cost])
    writer.writerow(['Pump', pump_cost])
    writer.writerow(['Sensors', sensor_cost])
    writer.writerow(['Total Cost', total_cost])
    writer.writerow([])
    writer.writerow(['Estimated Monthly Yield (lbs)', estimated_yield])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=GrowHome_Report.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
