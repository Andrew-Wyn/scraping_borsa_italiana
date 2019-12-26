import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

from data import *

logging.basicConfig( level=logging.DEBUG, filename='tmp/borsa.log', filemode="w")
logger = logging.getLogger('flaskServer')


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

    recapFile = open("tmp/recapFile.txt", "w+")

    
    recapFile.write("RISULTATI ULTIMA RICERCA\ndate -> " + str(datetime.now()) + "\n\n")
    logger.info("--- ricerca ---")
    logger.info("date: " + str(datetime.now()))

    for result in results:
        r = requests.get(
            results[0].get('link')  
            )

        soup = BeautifulSoup(r.text, 'html.parser')

        tableScraped = soup.find_all('table', {'class': 'm-table'})[0]

        spans = tableScraped.find_all('span')

        action = mainAlgorithm(
                Action(
                    result.get('title'),
                    float(spans[1].text.replace(',','.')),
                    float(spans[3].text.replace(',','.')),
                    float(spans[5].text.replace(',','.')),
                    float(spans[7].text.split(" - ")[0].replace(',','.')),
                    float(spans[9].text.split("  - ")[0].replace(',','.')) 
                )
            )
        
        recapFile.write(action.toString())
        logger.info(action.toString())

        statistics.append(
            action
        )
    
    recapFile.close()
    logger.info("--- end ---")

    return statistics

# capire se renderlo un metodo di Action

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