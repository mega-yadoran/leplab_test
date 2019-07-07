from pymongo import MongoClient
from dateutil.tz import gettz
import pytz
import dateutil.parser
import datetime

client = MongoClient('localhost', 27017)
 
db = client.mydb
 
cnt = 0
for record in db.test.find():
    cnt += 1
    dt = record['created_at']
    print ('----',dt)
    print (record['text'])
