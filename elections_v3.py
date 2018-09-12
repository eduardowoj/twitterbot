#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:12:16 2018

@author: eduardo
"""
# Importando as bibliotecas
import nltk
import re
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_predict

# Antes de começar a pegar novos tweets e processá-los, vou criar e treinar
# um classificador. Este usa um conjunto de dados de tweets pré-classificados,
# relacionados à política, em positivos, negativos e neutros. 
# Este conjunto de dados foi obtido de https://github.com/minerandodados/mdrepo

# Lê e prepara o csv
dataset = pd.read_csv('Tweets_Mg.csv')

# O dataset contém muita informação, mas não precisamos de tudo. Queremos
# apenas treinar nosso algoritmo para compreender palavras que transmitem
# sentimentos positivos, negativos e neutros, especificamente num contexto
# de política, o que é relevante para nosso objetivo.

# Vamos separar apenas o texto dos tweets e seus sentimentos
tweets = dataset['Text'].values
sentimentos = dataset['Classificacao'].values

# Muitos algoritmos de sentiment analysis limpam as amostras de texto para
# manter apenas substantivos (tokenização), e eliminam as terminações 
# (stemming) por questões de otimização. No entanto, quando estamos tratando
# de opiniões, isso frequentemente não é o melhor a se fazer: Ao remover 
# palavras como "não", por exemplo, é possível errar completamente o sentido
# da frase. Então vamos desenvolver um modelo de bag of words.

# O modelo bag of words é mais indicado aqui por que vai treinar o classifi-
# cador não só para reconhecer palavras específicas mas também para avaliar
# o sentimento de acordo com a freqüência de algumas palavras.

# Vamos por partes, então, criando alguns objetos

# O objeto vectorizer separa cada tweet em palavras individuais e 
# calcula suas freqüências
vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(tweets)

# Criamos e ajustamos então um modelo baseado em Naïve-Bayes para as
# frequencias de palavras
classificador = MultinomialNB()
classificador.fit(freq_tweets,sentimentos)

# Ao invés de checarmos a acurácia desse modelo com uma simples implementação,
# vamos partir direto para uma validação cruzada, que é muito mais robusta.

validacao = cross_val_predict(classificador, freq_tweets, sentimentos, cv=10)

# Finalmente, podemos estimar a acurácia
acuracia = metrics.accuracy_score(sentimentos, validacao)
print(acuracia)

# E analisar outras métricas de precisão também
tipos=['Positivo','Negativo','Neutro']
print (metrics.classification_report(sentimentos,validacao,tipos),'')

# Vamos analisar também a confusion matrix, que pode nos dizer um pouco mais.
# É uma análise interessante pois ela pode nos mostrar se o modelo é enviesado
# para algum lado, isto é, se tem mais falsos positivos ou mais falsos negati-
# vos (ou ainda, falsos neutros, no nosso caso).

# Para tanto, usamos o método crosstab do Pandas, que cria uma tabulação
# cruzada de fatores. É mais interessante que simplesmente importar o módulo
# de confusion matrix do sklearn pois desta forma temos mais controle sobre
print (pd.crosstab(sentimentos, validacao, rownames=['Real'], colnames=['Previsão'], margins=True), '')
 
# Disso vemos logo que de 2446 tweets negativos, o classificador acertou 2275,
# ou 93%. Dos restantes, classificou 162 como neutros e 9 como positivos.
# Neutros e Positivos não tiveram o mesmo sucesso, mas também não foram mal.
# De 2453 tweets neutros, o preditor acertou 2067, considerou 146 como falsos
# positivos e 240 como falsos negativos. De 3300 positivos, considerou 356
# como falsos neutros e 45 como falsos negativos.

# Uma maneira de melhorar a acurácia é usando bigramas, ao invés de monogramas.
# Isto é uma maneira chique de dizer que ao invés o modelo ajustar palavras 
# individuais, vai trabalhar com duplas de palavras. Isso permite que termos que
# são decididamente positivos ou negativos possam também acompanhar outras 
# palavras, dando mais robustez ao modelo. 
# Implementar isso é surpreendentemente simples. Basta modificar nosso vetori-
# zador para construir duplas de palavras. Assim ao invés de quebrar uma frase
# como "A chuva cai do céu" em [A,chuva,cai,do,céu], temos [A chuva, chuva cai,
# cai do, do céu].

# Repetindo então as linhas acima

vectorizer = CountVectorizer(ngram_range=(1,2))
freq_tweets = vectorizer.fit_transform(tweets)

# Implementamos o mesmo classificador, que agora trabalhará com os bigramas
classificador = MultinomialNB()
classificador.fit(freq_tweets,sentimentos)

# E voilà! Vamos checar a acurácia novamente, reimplementando as linhas aqui
validacao = cross_val_predict(classificador, freq_tweets, sentimentos, cv=10)

# Finalmente, podemos estimar a acurácia
acuracia = metrics.accuracy_score(sentimentos, validacao)
print(acuracia)

# E analisar outras métricas de precisão também
tipos=['Positivo','Negativo','Neutro']
print (metrics.classification_report(sentimentos,validacao,tipos),'')

# E, finalmente, a nova matriz de confusão
print (pd.crosstab(sentimentos, validacao, rownames=['Real'], colnames=['Previsão'], margins=True), '')
 
# Antes tínhamos 88.31% de acurácia, e agora temos 89.55%. Uma ligeira melhora,
# puxada pela melhora considerável na classificação dos tweets neutros, apesar
# de não ter mudanças significativas nos negativos e positivos. Agora, com o
# modelo treinado, podemos começar a experimentar em nossos tweets políticos!

# Vamos começar importando o necessário para usar a API do Twitter
import tweepy
import json

# E autenticar meu usuário
consumer_key = 'vK4CEfP9M2bZ9nFwTukgyQyvO'
consumer_secret = 'CvbeLGl4ODLFWi5neipzJElqU0uQwrJNHCdAOqC8lvjtcvtx3b'

access_token = '58244010-qmVXU9brlxnUPVsh7udTXLMNS6SKE06qbIfBpVVoa'
access_token_secret = 'a67Otn7k0BbRuDCrUGr6c8zICjCfvSN7SAEJ9D6iWnk8Y'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

# Vamos agora criar uma lista com alguns nomes de candidatos
candidatos = ['Bolsonaro', 'Amoedo']
dict_nomes = dict(enumerate(candidatos))

# E uma variável com o número de tweets que queremos
numTweets = 25

# O loop que pega os tweets e cria dataframes é um tanto complexo, mas funciona
# O objetivo é construir um dataframe com todas as informações do json, já
# que isso me dará uma flexibilidade muito maior para lidar com os dados

lista_dicts = []

for nome in candidatos:
    print(nome)
    # Pega os tweets para o candidato 'nome' da lista 'candidatos'
    
    # Vamos pegar apenas tweets originais, e excluir retweets
    # que podem enviesar nossa análise
    query = nome + " -filter:retweets"
    tweets = api.search(query, count=numTweets)    
    # Cria um dataframe para cada um
    #dict_nomes[nome] = pd.DataFrame()   
    for tweet in tweets:
        lista_dicts.append(tweet._json)
    # Para cada candidato, cria um arquivo de texto e faz o dump
    # dos conteúdos do json para ele    
    with open('tweets_%s.txt' % nome, 'w') as file:
        file.write(json.dumps(lista_dicts, indent=4))
    # Transforma o txt em dataframe
    my_demo_list = []
    with open('tweets_%s.txt' % nome, encoding='utf-8') as json_file:  
        all_data = json.load(json_file)
        # Zera o dataframe
        my_demo_list = []
        for each_dictionary in all_data:
            tweet_id = each_dictionary['id']
            whole_tweet = each_dictionary['text']
            only_url = whole_tweet[whole_tweet.find('https'):]
            favorite_count = each_dictionary['favorite_count']
            created_at = each_dictionary['created_at']
            whole_source = each_dictionary['source']
            only_device = whole_source[whole_source.find('rel="nofollow">') + 15:-4]
            source = only_device
            coordinates = each_dictionary['coordinates']

            my_demo_list.append({'name': str(nome),
                                 'tweet_id': str(tweet_id),
                                 'favorite_count': int(favorite_count),
                                 'url': url,
                                 'created_at': created_at,
                                 'source': source,
                                 'text': str(whole_tweet),
                                 'coordinates': coordinates,
                                 })
            # Salva no dataframe apropriado
            tweet_json = pd.DataFrame(my_demo_list, columns = ['name','tweet_id', 'favorite_count', 
                                                               'created_at',
                                                               'text', 'coordinates'])
            
    #dict_nomes[nome] = tweet_json.copy(deep=True)




