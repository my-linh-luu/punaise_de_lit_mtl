from flask import Flask, render_template, request, redirect, make_response, g, jsonify
from flask.helpers import url_for
import sqlite3
import pandas as pd
import requests
from io import StringIO
from apscheduler.schedulers.background import BackgroundScheduler
from flask_json_schema import JsonSchema, JsonValidationError

from .database import Database
from .declaration import Declaration
# import re
# import datetime
# from datetime import date
# from calendar import month, monthrange
# from dateutil.relativedelta import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # what for?
scheduler = BackgroundScheduler()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({'error': e.message, 'errors': errors}), 400


@scheduler.scheduled_job('cron', hour=0)
def fetch_data_periodically():
    connection = sqlite3.connect("db/data.db")
    csv_url = 'https://data.montreal.ca/dataset/49ff9fe4-eb30-4c1a-a30a-fca82d4f5c2f/resource/6173de60-c2da-4d63-bc75-0607cb8dcb74/download/declarations-exterminations-punaises-de-lit.csv'
    s = requests.get(csv_url).content
    df = pd.read_csv(StringIO(s.decode('utf-8')))
    df.to_sql('data', con=connection, if_exists='replace', index=False)
    print("fetching...")  # a enlever


scheduler.start()


@app.route("/doc")
def get_doc():
    return render_template("doc.html")


@app.route("/", methods=["POST", "GET"])
def accueil():
    if request.method == "GET":
        return render_template("accueil.html")
    else:  # POST
        recherche = request.form["recherche"]
        if recherche == "":
            return render_template("accueil.html", error="Veuillez entrer une valeur.")
        else:
            resultats = get_db().get_all_by_nom_qr_or_nom_arr(recherche)
            if not resultats:  # si dictionnaire est vide, affiche false et ne rentrera pas dans cette condition
                return render_template("accueil.html", error="Aucun résultat correspondant à votre recherche.")
            else:
                return redirect(url_for('get_declarations_by_nomqr_nomarr', recherche=recherche))


@app.route("/resultats/<recherche>")
def get_declarations_by_nomqr_nomarr(recherche):
    resultats = get_db().get_all_by_nom_qr_or_nom_arr(
        recherche)  # on retrouve les donnees
    return render_template("recherche.html", recherche=resultats)


@app.route("/api/declarations", methods=["GET"])
def get_declarations_by_dates():
    declarations = get_db().get_all_in_between_dates(
        '2013-01-01', '2014-01-01')  # a changer
    return jsonify([declaration.build_dictionary_all() for declaration in declarations])


# def entre_date():
#     resultats = get_db().get_all_in_between_dates('2011-01-01', '2012-12-01')
#     return render_template("recherche.html", recherche = resultats)
