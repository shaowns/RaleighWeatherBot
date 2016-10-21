
# coding: utf-8

# In[1]:

import logging
import tweepy
import forecastio
import argparse
from keys import *


# In[2]:

def setup_twitter_api():
    """Initiate the twitter api. Call this function once at the beginning and use the returned api object."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


# In[3]:

def setup_logging():
    """Initiates basic logger"""
    logger = logging.getLogger('raleigh_weather_bot')
    hdlr = logging.FileHandler('./raleigh_weather_bot.log', mode='a')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    return logger


# In[4]:

def get_tweets(w):
    """Get tweetable sentences from the summary forecast"""
    tweets = list()
    basic = "Currently {}, temp {}, humidity at {}, feels like {}."             .format(w['summary'], w['temp'], w['humidity'], w['feelslike'])    
    tweets.append(basic)
    return tweets


# In[12]:

def do_tweet(tweets, api, logger):
    for t in tweets:
        try:
            api.update_status(t)
            logger.info("Tweeting: {}".format(t))
        except Exception as e:
            logger.error("Exception: {}, Tweet: {}".format(str(e), t))


# In[6]:

def get_hourly_tweets(logger):
    blob = forecastio.get_forecast(logger)
    w = forecastio.parse_forecast(blob)
    tweets = get_tweets(w)
    return tweets


# In[9]:

def main():
    ap = argparse.ArgumentParser(description='Raleigh Weather Bot')
    ap.add_argument('-t', action='store_true', help='Make a tweet about current weather forecast', default=True)
    args = ap.parse_args()
    
    logger = setup_logging()
    
    tweets = list()
    if args.t:
        tweets = get_hourly_tweets(logger)
    
    twitter_api = setup_twitter_api()
    do_tweet(tweets, twitter_api, logger)
    return


# In[ ]:

if __name__ == '__main__':
    main()

