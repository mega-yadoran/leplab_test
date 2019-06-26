# -*- coding: utf-8 -*-

from pymongo import MongoClient
# http://ailaby.com/twitter_api/#id6_1 のソースを
# twitterAPI.py で保存
from twitterAPI import TweetsGetter

client = MongoClient('localhost', 27017)

db = client.mydb

tweets = TweetsGetter.bySearch(u'渋谷').collect(total=500)
for tweet in tweets:
    tweet2 = {}
    tweet2['id'] = tweet['id']
    tweet2['text'] = tweet['text']
    tweet2['created_at'] = tweet['created_at']
    tweet2['user'] = {'screen_name' : tweet['user']['screen_name']}

    db.shibuya.insert(tweet2)

# test
# test2