#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:12:16 2018

@author: eduardo
"""
import tweepy
from textblob import TextBlob
from textblob.exceptions import NotTranslated
from textblob.translate import Translator

consumer_key = 'vK4CEfP9M2bZ9nFwTukgyQyvO'
consumer_secret = 'CvbeLGl4ODLFWi5neipzJElqU0uQwrJNHCdAOqC8lvjtcvtx3b'

access_token = '58244010-qmVXU9brlxnUPVsh7udTXLMNS6SKE06qbIfBpVVoa'
access_token_secret = 'a67Otn7k0BbRuDCrUGr6c8zICjCfvSN7SAEJ9D6iWnk8Y'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)


#print(api.me())
tweets = api.search('Bolsonaro')

for tweet in tweets:
    frase = TextBlob(tweet.text)

    if frase.detect_language() == 'pt':
        traducao = TextBlob(str(frase.translate(from_lang='pt', to='en')))
        print('Tweet: {0} - Sentimento: {1}'.format(tweet.text, traducao.sentiment))
    else:
        print('Tweet: {0} - Sentimento: {1}'.format(tweet.text, frase.sentiment))