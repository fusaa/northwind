import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import pandas as pd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Using SQL CS50 lib
db = SQL("sqlite:///data.db")


@app.after_request
def after_request(response):
    """Ensures that responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@app.route("/index.html")
# @login_required
def index():
    # return render_template("content/index.html")
    return render_template("content/index2.html")

@app.route("/2")
@app.route("/index2.html")
# @login_required
def index2():
    return render_template("content/index2.html")

@app.route("/orders.html")
@app.route("/orders")
# @login_required
def orders():
    # query db for last X orders
    # build html
    orders = query_order()
    return render_template("content/orders.html", orders=orders)

def query_order():
    query = """
    SELECT

    """
    result = db.execute("SELECT * FROM Orders;")  # TODO: include LIMIT 100 ... ?
    # convert json output to pandas and then html
    # df = pd.read_json(result, orient='columns') # 'columns' is the default orientation
    df = pd.DataFrame(result)

    df['OrderID'] = df['OrderID'].apply(lambda x: f'<form action="order_detail" method="post"><button type="submit" name="order_id" value="{x}" class="number-button">{x}</button></form>')


    html_table = df.to_html(index=False, table_id = 'datatablesSimple', border = 0, escape = False)

    # Output the HTML table
    print(html_table)
    # print(type(result))
    # print(result)
    return(html_table)

