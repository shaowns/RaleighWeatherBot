# coding: utf-8

# In[27]:

from urllib2 import urlopen, URLError
import json
from keys import FORECASTIO_KEY


# In[25]:

def get_forecast(logger):
    """Retrive forecast from Forecast.io for Raleigh, NC"""
    RALEIGH = '35.787743,-78.644257'

    url = "https://api.forecast.io/forecast/{}/{}?exclude=minutely,daily,flags".format(FORECASTIO_KEY, RALEIGH)

    try:
        resp = urlopen(url)
    except URLError:
        logger.log("URLError when trying to hit the Forecast.io API.", logging.ERROR)
    else:
        r = resp.read().decode('utf-8')
        return json.loads(r)


# In[26]:

def parse_forecast(blob):
    """Extract the necessary information from the forecast json data"""
    w = dict()
    cur = blob['currently']
    w['summary'] = cur['icon'].replace('-', ' ')
    w['temp'] = str(int(round(cur['temperature'], 0))) + '°F'
    w['humidity'] = str(cur['humidity'] * 100) + '%'
    w['feelslike'] = str(int(round(cur['apparentTemperature']))) + '°F'
    return w
