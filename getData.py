# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:55:58 2015

@author: zxgcqupt
"""
from yahoo_finance import Share
import csv
import os
stock_list=[]
with open('stock_list.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stock_list.append(row['Symbol'])

os.remove('stockdata.json')
for i in range(0,1):
    yahoo=Share(stock_list[i]) 
    print 'current record is'+str(i) 
    try: 
    	data=yahoo.get_historical('1900-02-20', '2015-03-31')
    	for j in range(0,len(data)):
            obj = open("stockdata.json","a")
            obj.write(str(data[j])+'\n')
            obj.close
    except:
	pass
