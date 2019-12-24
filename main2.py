import requests
from bs4 import BeautifulSoup
from urllib import parse
from flask import Flask
from flask_restful import Resource, Api, reqparse
import logging
from datetime import datetime
import re
import enum
import json
from json import JSONEncoder
from flask import render_template
from flask import request


app = Flask(__name__)
api = Api(app)

logging.basicConfig( level=logging.DEBUG, filename='borsa.log')

class Status(enum.Enum): 
    BUY = "BUY"
    SELL = "SELL"
    NOTHING = "NOTHING"

class Action(object):
    def __init__(self, title, aperture, max_oggi, min_oggi, max_anno, min_anno):
        self.title = title
        self.aperture = aperture
        self.max_oggi = max_oggi
        self.min_oggi = min_oggi
        self.max_anno = max_anno
        self.min_anno = min_anno
        self.status = None

    def setStatus(self, status):
        self.status = status

# ------ UTILITY FUNCTIONS

def getSearchResults(term, pages):

    pages = int(pages)

    r = requests.get(
        'https://www.borsaitaliana.it/borsa/searchengine/search.html?lang=it&q={}'.format(term)     
        )

    soup = BeautifulSoup(r.text, 'html.parser')

    resultsRow = soup.find_all('tr', {"class": None})

    results = []

    count = 1

    for resultRow in resultsRow:

        

        if count > pages:
            break

        link = resultRow.find("a", {'class': 'u-hidden'}).get('href')
        title = re.sub('(\n|\t|\r)', '', resultRow.find("a", {'class': 'u-hidden'}).find('span', {'class': 't-text'}).text)
        portfoglio = resultRow.find('span', {'class': '-portfolio-xs'})
        
        if portfoglio != None:
            results.append({
                'link': link,
                'title': title
            })

        count += 1
    
    return results



def getStatisticsFromResults(results):
    
    statistics = []

    for result in results:
        r = requests.get(
            results[0].get('link')  
            )

        soup = BeautifulSoup(r.text, 'html.parser')

        tableScraped = soup.find_all('table', {'class': 'm-table'})[0]

        spans = tableScraped.find_all('span')

        statistics.append(
            mainAlgorithm(
                Action(
                    result.get('title'),
                    float(spans[1].text.replace(',','.')),
                    float(spans[3].text.replace(',','.')),
                    float(spans[5].text.replace(',','.')),
                    float(spans[7].text.split(" - ")[0].replace(',','.')),
                    float(spans[9].text.split("  - ")[0].replace(',','.')) 
                )
            )
        )

    return statistics

def mainAlgorithm(action):
    annualMean = (action.min_anno + action.max_anno)/2

    percent = annualMean/10

    todayMean = (action.min_oggi + action.max_oggi)/2

    if todayMean > (annualMean + percent):
        action.setStatus(Status.SELL)
    elif todayMean < (annualMean - percent):
        action.setStatus(Staus.BUY)
    else:
        action.setStatus(Status.NOTHING)
    
    return action

# ------------------------------------------

# ----- class for flask meta-framework

actions = []

@app.route("/borsa")
def mainSearch():
    global actions

    term = request.args.get('term', type = str)
    pages = request.args.get('pages', default = 1, type = int)

    actions = getStatisticsFromResults(getSearchResults(term, pages))
    
    return render_template("table.html", actions = actions)

@app.route("/")
def index():
    print(actions)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)