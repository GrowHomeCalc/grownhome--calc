@echo off
echo Starting Flask App...
set FLASK_APP=myapp.py
set FLASK_ENV=development
python -m flask run
