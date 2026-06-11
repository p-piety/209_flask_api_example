from flask import Flask, render_template,  request
import pandas as pd
import os
import sqlite3 

# IMPORTANT: fix paths for serverless environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

@app.route("/")
def hello():
    return render_template("w209.html")

@app.route("/getData/<int:year>")
def getData(year):
    csv_path = os.path.join(STATIC_DIR, "data", "1_Revenues.csv")
    revenue = pd.read_csv(csv_path)

    if year < 1942 or year > 2008:
        return "Error in the year range"

    filteredRevenue = revenue[revenue['Year4'] == year][[
        "Name", "Year4", "Total Revenue", "Population (000)"
    ]]

    return filteredRevenue.to_json(orient='records')

@app.route("/api")
def api():
    return {"x": 20}

@app.route("/players/count")
def count_players():
    con = sqlite3.connect("api/players/count/players_20.db")
    cur = con.cursor()
    result = cur.execute("SELECT COUNT(*) FROM players")
    return {"count": result.fetchone()[0]}


@app.route("/players/get_nationality")
def get_nationality():
    con = sqlite3.connect("api/players/count/players_20.db")
    cur = con.cursor()
    player = request.args.get('player')
    nationality = request.args.get('nationality')
    #not best practice, needs to validate that there are not SQL injection attempts, but for demo purposes this is fine
    result = cur.execute("SELECT COUNT(*) FROM players WHERE nationality = ?", (nationality,))
    return {"count": result.fetchone()[0]}

#get_nationality?nationality=Argentina

# Vercel entry point
def handler(request, response):
    return app(request.environ, response)
