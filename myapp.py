
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/design')
def design():
    return render_template("design.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

@app.route('/compare-breakeven')
def compare_breakeven():
    return render_template("compare-breakeven.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/setup')
def setup():
    return render_template("setup.html")

@app.route('/calculations')
def calculations():
    return render_template("calculations.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
