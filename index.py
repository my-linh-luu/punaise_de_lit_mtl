from flask import Flask, render_template, request, redirect, make_response, g
from flask.helpers import url_for
from .database import Database
# import re
# import datetime
# from datetime import date
# from calendar import month, monthrange
# from dateutil.relativedelta import *

app = Flask(__name__)


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

@app.route("/", methods=["POST", "GET"])
def accueil():
    if request.method == "GET":
        return render_template("layout.html")
