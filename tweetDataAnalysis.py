# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 20:38:40 2015

@author: zxgcqupt
"""
from pyspark.sql import SQLContext
from pyspark.sql import *
import json
import time
import re
## load data
def process(s):
    s = json.loads(s);
    try:
        timestamp = time.strptime(s['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet_time = str(timestamp.tm_year)
        if timestamp.tm_mon<10:
            tweet_time = tweet_time + '0' + str(timestamp.tm_mon)
        else:
            tweet_time = tweet_time + str(timestamp.tm_mon)
        if timestamp.tm_mday<10:
            tweet_time = tweet_time + '0' + str(timestamp.tm_mday)
        else:
            tweet_time = tweet_time + str(timestamp.tm_mday)
    except: 
        tweet_time='20150430'
    try:
        content = re.sub(r'[^a-zA-Z0-9]',' ',s['text'].encode('utf-8').strip())
    except:
        content = ' '
    return content, tweet_time

path = 'tweets_af'
tweet = sc.textFile(path).map(process)

sqlContext = SQLContext(sc)
schemaString = "text created_at"

fields = [StructField(field_name, StringType(), False) for field_name in schemaString.split()]
schema = StructType(fields)

schemaTweet = sqlContext.applySchema(tweet, schema)

schemaTweet.registerTempTable("tweet")

#text = sqlContext.sql("SELECT count(1) FROM tweet WHERE text like '%upset%' and created_at = 20140609")
text = sqlContext.sql("SELECT count(1), created_at FROM tweet GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%hope%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%happy%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%fear%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%worry%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%nervous%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%anxious%' GROUP BY created_at")
#text = sqlContext.sql("SELECT count(1), created_at FROM tweet WHERE text like '%upset%' GROUP BY created_at")

text.collect()