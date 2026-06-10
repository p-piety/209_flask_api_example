# from flask import Flask, render_template
# app = Flask(__name__)
# import pandas as pd
# import os

# APP_FOLDER = os.path.dirname(os.path.realpath(__file__))

# @app.route("/")
# def hello():
#     return render_template("w209.html")

# @app.route("/getData/<int:year>")
# def getData(year):
#     # Load the CSV file from the static folder, inside the current path
#     revenue = pd.read_csv(os.path.join(APP_FOLDER,"static/data/1_Revenues.csv"))

#     if year < 1942 or year > 2008:
#         return "Error in the year range"

#     filteredRevenue = revenue[revenue['Year4']==year][["Name","Year4", "Total Revenue","Population (000)"]]

#     # show the post with the given id, the id is an integer
#     return filteredRevenue.to_json(orient='records')

from flask import Flask, render_template
import pandas as pd
import os

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

# Vercel entry point
def handler(request, response):
    return app(request.environ, response)
