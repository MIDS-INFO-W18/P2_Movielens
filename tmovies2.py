# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 07:57:00 2018

@author: SYSTEM
"""
import os
import csv
import pandas as pd
import numpy as np

os.chdir(r'D:\GitHub\python_course\P2_Movielens')

movies=pd.read_csv("ml-dataset/movies.csv")

links=pd.read_csv("ml-dataset/links.csv")
links.head(10)

ratings=pd.read_csv('ml-dataset/ratings_small.csv')

last_10yr_id = pd.read_csv('mID.csv', header=None)

last_10yr_id = last_10yr_id[0]

tID = links[links.movieId.isin(last_10yr_id)].tmdbId

import tmdbsimple as tmdb
tmdb.API_KEY = 'b93b517fa262fe2fdf374829ee9e2fb5'

#https://pypi.org/project/ratelimiter/

from ratelimiter import RateLimiter

#movie = tmdb.Movies(603)
movie = tmdb.Movies(tID.iloc[0])
tmovies = pd.DataFrame.from_dict(movie.info(), orient='index')

rate_limiter = RateLimiter(max_calls=4, period=1)

checklist = []
count=0
length = len(tID)
for id in tID.iloc[1:]:
    try:
        with rate_limiter:
            movie = tmdb.Movies(id)
            tmovies = pd.concat([tmovies, pd.DataFrame.from_dict(movie.info(), orient='index')], axis=1 )
            print(count, 'of', length)
            count += 1
    except:
        checklist.append(id)
        count += 1
        
        
tmovies = tmovies.transpose()
tmovies.to_csv('tmovies.csv')

print(checklist)