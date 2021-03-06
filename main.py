# -*- coding: utf-8 -*-
"""
Created on Fri May 01 19:43:13 2015

@author: baoy
"""


#################################################################################

#############  Multivariate Regression model ##############
 
#################################################################################

from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
# import matplotlib.pyplot as plt

import statsmodels.api as sm

import matplotlib.pyplot as plt

from datetime import datetime
from statsmodels.graphics.api import qqplot
import csv




# print (sm.datasets.sunspots.NOTE)

df_adv = pd.read_csv('outputData.csv', index_col=0)

X = df_adv[['coffeevalue','coppervalue','cottonetfvalue','glodvalue','nasdaqvixsettle','gasclose','crudeoilsettle','beanclose','wheatclose']]
y = df_adv['spvixclose']
df_adv.head()


# fit an OLS model with intercept on TV and Radio
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()

print(est.summary())

Weights = est.params


#################################################################################

#############  ARMA model ##############
 
#################################################################################






### loadData ###
dataSet = pd.read_csv('outputData.csv') #, index_col=0)


f = open('outputData.csv', 'rb')
reader = csv.reader(f)
headers = reader.next()

val =[]

for i in range(1,len(headers)):
    if i !=8:
        dta = dataSet[["date", headers[i]]]

        dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001', '2237'))
        del dta["date"]



        dta.plot(figsize=(12,8))

        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(211)
        
        fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

        arma_mod50 = sm.tsa.ARMA(dta, (5,0)).fit()
        print(arma_mod50.params)
        

        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)
        ax = arma_mod50.resid.plot(ax=ax)
        #plt.savefig(headers[i]+'.jpg')       
        sm.stats.durbin_watson(arma_mod50.resid.values)
        resid = arma_mod50.resid
        stats.normaltest(resid)
        
        r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
        
        data = np.c_[range(1,41), r[1:], q, p]
        
        table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
        
        print(table.set_index('lag'))

        predict_stock = arma_mod50.predict('2237', '2241', dynamic=True)
        
        val.append(predict_stock)
        
        
        
        
#######################################
    ###     predicted values    ###        
#######################################

predVec = np.array(val)

weight = Weights[1:10]
const = Weights[0]

w = weight.reshape(1, 9)

# prediction about S&P500 Index on the following days
predResult_oneDayLater = np.dot(w, predVec[:, 0]) + const

predResult_twoDayLater = np.dot(w, predVec[:, 1]) + const

predResult_threeDayLater = np.dot(w, predVec[:, 2]) + const

predResult_fourDayLater = np.dot(w, predVec[:, 3]) + const

predResult_fiveDayLater = np.dot(w, predVec[:, 4]) + const
