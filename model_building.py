# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

df = pd.read_csv('C:/Users/shahb/gd_salary_pred_jupyter/cleaned_data2.csv')

# choose relevant columns
df_model = df[['Rating','avg_size','Type of ownership','Industry',
            'Sector','num_comp','age','job_simp','seniority','desc_len',
            'state','python_yn','spark_yn','aws_yn','hadoop_yn']]

# get dummy variables

df_dum = pd.get_dummies(df_model)

# train test set
y = df.avg_salary.values
X = df_dum

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=222)
# Multiple linear regression
import statsmodels.api as sm

X_sm = X= sm.add_constant(X)

model = sm.OLS(y, X_sm)

model.fit().summary()

from sklearn.linear_model import LinearRegression,Lasso
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

lm = LinearRegression()

lm.fit(X_train,y_train)
cross_val_score(lm,X_train,y_train,scoring='neg_mean_absolute_error',cv=3)

# Lasso regression
lm_l = Lasso(alpha=.68)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))


alpha = []
error = []

for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha=i/100)
    error.append(np.mean(cross_val_score(lml,X_train,y_train,scoring='neg_mean_absolute_error',cv=3)))

plt.plot(alpha,error)

min_error_ind = np.argmax(error)
alpha[min_error_ind]

# Random Forest

rf = RandomForestRegressor()

cross_val_score(rf,X_train,y_train,scoring='neg_mean_absolute_error',cv=3)
# tune using gridsearchcv
from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

print(gs.best_score_)

print(gs.best_estimator_)


# test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lml+tpred_rf)/2)