import data
from flask import Flask
import requests
from urllib import parse
import logging
from datetime import datetime
from flask import render_template
from flask import request
from flask import send_file

from data import *
from utilities import *


# global variables

logging.basicConfig( level=logging.DEBUG, filename='tmp/borsa.log', filemode="w")
logger = logging.getLogger('flaskServer')
app = Flask(__name__)

# -------------------------------------------


@app.route("/borsa", methods = ['GET'])
def mainSearch():
    global actions

    term = request.args.get('term', type = str)
    pages = request.args.get('pages', default = 1, type = int)

    actions = getStatisticsFromResults(getSearchResults(term, pages))
    
    return render_template("table.html", actions = actions)

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/download', methods = ['GET'])
def downloadFile ():
    path = "tmp/recapFile.txt"
    print("sdasd")
    return send_file(path, as_attachment=True)