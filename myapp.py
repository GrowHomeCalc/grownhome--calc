
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = request.form if request.method == 'POST' else {}
    return render_template("index.html", form=form)

@app.route('/design')
def design():
    return render_template("design.html")

@app.route('/setup')
def setup():
    return render_template("setup.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

@app.route('/compare-breakeven')
def compare_breakeven():
    return render_template("compare-breakeven.html")

@app.route('/calculations')
def calculations():
    return render_template("calculations.html")

@app.route('/download-pdf')
def download_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "GrowHome Calc PDF Summary")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='summary.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
