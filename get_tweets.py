# -*- coding: utf-8 -*-
import csv
from pymongo import MongoClient
from dateutil.tz import gettz
import dateutil.parser
import datetime
import pytz
# http://ailaby.com/twitter_api/#id6_1 のソースを
# twitterAPI.py で保存
from twitterAPI import TweetsGetter

# DB接続
client = MongoClient('localhost', 27017)
db = client.mydb

# CSV読み込み
# csv_file = open("./document/words.csv", "r", encoding="ms932", errors="", newline="" )
# words = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
# print(words)

csv_file = open('./document/words.csv', 'r')
words = csv.reader(csv_file)

cnt = 0
for word in words:
    # 指定ワードを含むツイートを検索
    print('-----------------')
    print(word[0] + 'を含むツイートの取得を開始します')
    tweets = TweetsGetter.bySearch(word[0] + u' -bot').collect(total=280)

    # 見つけたユーザーの最新48時間のツイートを取得
    for tweet in tweets:
        cnt += 1

        # 取得するツイートの時刻条件
        score_border_datetime = (datetime.datetime.now() + datetime.timedelta(days=-1)).astimezone(gettz('Asia/Tokyo')) # スコアになる境界の時刻
        input_border_datetime = (datetime.datetime.now() + datetime.timedelta(days=-7)).astimezone(gettz('Asia/Tokyo')) # 取得する境界の時刻

        tweets2 = TweetsGetter.byUser(tweet['user']['id']).collect(total=500)
        for tweet2 in tweets2:
            tw = {}
            tw['sample_id'] = cnt
            tw['user_id'] = tweet['user']['id']
            tw['text'] = tweet2['text']

            # 日付のフォーマット
            tweet2_day = (dateutil
                .parser
                .parse(tweet2['created_at'])
                .astimezone(gettz('Asia/Tokyo')))
            tw['created_at'] = tweet2_day.strftime("%Y-%m-%d %H:%M:%S")

            # 当日のツイート
            if tweet2_day > score_border_datetime:
                db.score_tw.insert_one(tw)
            # 前日のツイート
            elif tweet2_day > input_border_datetime:
                db.input_tw.insert_one(tw)
            else:
                break

    # tweet2 = {}
    # tweet2['id'] = tweet['id']
    # tweet2['text'] = tweet['text']
    # tweet2['created_at'] = tweet['created_at']

    # db.shibuya.insert(tweet2)
