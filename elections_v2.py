#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:12:16 2018

@author: eduardo
"""
# Importando as bibliotecas
import tweepy
import nltk
import re
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords 
stopwords = stopwords.words('portuguese')
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

# Configurando acesso à API
consumer_key = 'vK4CEfP9M2bZ9nFwTukgyQyvO'
consumer_secret = 'CvbeLGl4ODLFWi5neipzJElqU0uQwrJNHCdAOqC8lvjtcvtx3b'

access_token = '58244010-qmVXU9brlxnUPVsh7udTXLMNS6SKE06qbIfBpVVoa'
access_token_secret = 'a67Otn7k0BbRuDCrUGr6c8zICjCfvSN7SAEJ9D6iWnk8Y'

# Autenticando
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Define emoticons, para processamento

# Positivos
emoticons_bom = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Negativos
emoticons_ruim = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# Todos emoticonts
emoticons = emoticons_bom.union(emoticons_ruim)

# Define função para limpar os tweets e prepará-los para análise

def limpaTweets(tweet):
    # Remove keyword RT, para retweet
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    # Remove os hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    
    # Remove os símbolos de hashtag
    tweet = re.sub(r'#', '', tweet)
 
    # Cria o tokenizador
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    
    # Tokeniza os tweets
    tweet_tokenized = tokenizer.tokenize(tweet)
 
    tweetsLimpos = []    
    for palavra in tweet_tokenized:
        if (palavra not in stopwords and # Remove as stopwords
              palavra not in emoticons and # Remove os emoticons
                palavra not in string.punctuation): # Remove pontuação
            #tweets_clean.append(word)
            stem_word = stemmer.stem(palavra) # Stemming
            tweetsLimpos.append(stem_word)
 
    return tweetsLimpos

##########
    
# Teste
# tweetTeste = "RT @Twitter Testando a API e o limpador de tweets :) #machinelearning #API http://google.com"
# print cleaned tweet
# print (limpaTweets(tweetTeste))
# Funcionando!!!

# Cria lista com hashtags de campanha
candidatos = ['bolsonaro','amoedo','ciro']

# Define quantos tweets queremos
numTweets = 5

# Loop principal
for nome in candidatos:
    tweet = nome
    #print(nome)
    tweets = api.search(nome,count=numTweets)
    for nome in tweets:
        # Cleaning the tweets
        print(limpaTweets(nome.text))

    
    # Tokenizing
    print(tweet_tokenizer.tokenize(tweet.text))
    
    
