import os
import pandas as pd
import numpy as np
import sqlalchemy
import MySQLdb
import config
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import json

app = Flask(__name__)


#################################################
# Database Setup
#################################################

engine = create_engine("mysql://root:" + config.password + "@localhost/bchi_db")
conn = engine.connect()

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/examples")
def example():
    """Return the examples page."""
    return render_template("examples.html")

@app.route("/sel_ind/<ind_cat_text>")
def ind_dd(ind_cat_text):
    # pull back all indicators that are in corrisponding category
    data = pd.read_sql(f"select distinct Indicator from bchi_data where Category like '{ind_cat_text}'", conn)
    dl_Ind = data["Indicator"].unique()
    ind_list = dl_Ind.tolist()
    return jsonify(ind_list)

@app.route("/sel_year/<ind_cat_text>/<ind_text>")
def year_dd(ind_cat_text, ind_text):
    #pull back all years in corrisponding category/indicator
    data = pd.read_sql(f"select distinct Year from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}'", conn)
    dl_Ind = data["Year"].unique()
    ind_list = dl_Ind.tolist()
    return jsonify(ind_list)

@app.route("/sel_sex/<ind_cat_text>/<ind_text>/<year_text>")
def sex_dd(ind_cat_text, ind_text, year_text):
    #pull back all genders in corrisponding category/indicator/year
    data = pd.read_sql(f"select distinct Sex from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}' and Year like '{year_text}'", conn)
    dl_Ind = data["Sex"].unique()
    ind_list = dl_Ind.tolist()
    return jsonify(ind_list)

@app.route("/sel_race/<ind_cat_text>/<ind_text>/<year_text>/<sex_text>")
def race_dd(ind_cat_text, ind_text, year_text, sex_text):
    #pull back all races in corrisponding category/indicator/year/sex
    data = pd.read_sql(f"select distinct Race from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}' and Year like '{year_text}' and Sex like '{sex_text}'", conn)
    dl_Ind = data["Race"].unique()
    ind_list = dl_Ind.tolist()
    return jsonify(ind_list)

@app.route("/sel_loc/<ind_cat_text>/<ind_text>/<year_text>/<sex_text>/<race_text>")
def loc_dd(ind_cat_text, ind_text, year_text, sex_text, race_text):
    #pull back all locations in corrisponding category/indicator/year/sex/race
    data = pd.read_sql(f"select distinct Location from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}' and Year like '{year_text}' and Sex like '{sex_text}' and Race like '{race_text}'", conn)
    dl_Ind = data["Location"].unique()
    ind_list = dl_Ind.tolist()
    return jsonify(ind_list)

@app.route("/sel_pie/<ind_cat_text>/<ind_text>/<year_text>/<sex_text>/<race_text>/<loc_text>/<data_text>")
def pie_data(ind_cat_text, ind_text, year_text, sex_text, race_text, loc_text, data_text):
    #pull back results for pie chart
    data = pd.read_sql(f"select {data_text}, Value from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}' and Year like '{year_text}' and Sex like '{sex_text}' and Race like '{race_text}' and Location like '{loc_text}' and Value > 0 group by {data_text}", conn)
    ind_list = data.values.tolist()
    return jsonify(ind_list)

@app.route("/sel_line/<ind_cat_text>/<ind_text>/<year_text>/<sex_text>/<race_text>/<loc_text>/<data_text>")
def line_data(ind_cat_text, ind_text, year_text, sex_text, race_text, loc_text, data_text):
    #pull back results for pie chart
    data = pd.read_sql(f"select {data_text}, Year, Value from bchi_data where Category like '{ind_cat_text}' and Indicator like '{ind_text}' and Year like '{year_text}' and Sex like '{sex_text}' and Race like '{race_text}' and Location like '{loc_text}' and Value > 0 group by {data_text}, Year", conn)
    ind_list = data.values.tolist()
    return jsonify(ind_list)

if __name__ == "__main__":
    app.run()
