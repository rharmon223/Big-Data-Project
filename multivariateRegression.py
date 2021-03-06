from __future__ import print_function
import numpy as np
from scipy import stats
import pandas as pd
# import matplotlib.pyplot as plt

import statsmodels.api as sm

# print (sm.datasets.sunspots.NOTE)

df_adv = pd.read_csv('outputData.csv', index_col=1)

X = df_adv[['coffeevalue','coppervalue','cottonetfvalue','glodvalue','nasdaqvixsettle','gasclose','crudeoilsettle','beanclose','wheatclose']]
y = df_adv['spvixclose']
df_adv.head()


# fit an OLS model with intercept on TV and Radio
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()

print(est.summary())

