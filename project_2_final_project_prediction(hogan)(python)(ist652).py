# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 13:26:09 2019
@author: BBE Brian hogan
Purpose: ist652 Prof. Landowski Final Project
Objective: to test building some multiple regression for "prediction"
aspect of the final project. This work is being done in Python for learning
even though randomForest, kNN, and naiveBanes are all built in R. As such,
may combine some work with R depending upon outcomes.
"""
##REQUIRED LIBRARIES FOR CALCULATIONS
import pandas as pd
import numpy as np
import xlsxwriter
import scipy
import matplotlib.pyplot as plt #plotting
import statsmodels.api as sm  #for getting p-values
from mpl_toolkits.mplot3d import Axes3D  #for 3d plots
from statsmodels.formula.api import ols #for statistics
from statsmodels.stats.anova import anova_lm #for analysis of variance
##file read csv in and nysb (New York State Bridges) data frame created
df0=pd.read_csv(r'C:\Users\BBE\Desktop\IST652+Scripting+Data+Analytic+(III)\Project+Final\Bri+Kat+Data\df1_prediction.csv')
df1 =pd.DataFrame(df0)
"""================ attempting to plot"""
    #x_value=np.array(df1['curb_to_curb_width_ft','deck_area_sq_ft'],np.float64.reshape(1,-1))
    #county+curb_to_curb_width_ft+deck_area_sq_ft+material+structure+year
"""end plot attempt===================dtype.fl==="""
df1.columns  #inspect fields for linear modeling
    #Index(['ID', 'region', 'county', 'lat', 'long', 'condition_rate',
    #       'inspection_date', 'bridge_length_ft', 'curb_to_curb_width_ft',
    #       'deck_area_sq_ft', 'aadt', 'year_of_aadt', 'material', 'structure',
    #       'year', 'popz'],
"""================================================================"""
"""==============LINEAR MODELING ================================="""
"""================================================================"""
"""fit the model"""
m1 = ols("condition_rate ~ region+county+lat+long+inspection_date+bridge_length_ft+curb_to_curb_width_ft+deck_area_sq_ft+aadt+year_of_aadt+material+structure+year+popz",df1).fit()
print(m1.summary()) #print model summary
#aov_table = sm.stats.anova_lm(m1,typ=2)  #anova_results = anova_lm(m1)
#print('/nANOVA RESULTS')
#print(aov_table) #varianve table measure
"""now add/subtract variables until find those w greatest influence"""
#moreve inspection date, bridgelenghtft,aadt, yearofaadt,(still at .787)
#4th wave removal:lat long(drop0.733); then region()+county drops to 0.26!
m2 = ols("condition_rate ~ county+curb_to_curb_width_ft+deck_area_sq_ft+material+structure+year",df1).fit()
print("Variable *county* plays a significant role in model's R2 calc")
print(m2.summary())

"""exporting regression results to a text file"""
import os
myfile =open('prediction.txt')
with open('myfile','w') as fh:
    fh.write(m2.summary().as_csv())  #writing the linear model to a file
myfile.close()
    
#these are all learning attempts to get to graph the equation that didnt work
        #"""graphing the model"""
        #    #from matplotlib import pyplot 
        #    #pyplot.scatter(m2)
        #
        #from sklearn.linear_model import LinearRegression
        #multiple_lr = LinearRegression()
        #multiple_lr.fit("condition_rate ~ county+curb_to_curb_width_ft+deck_area_sq_ft+material+structure+year",df1)
        #results =sm.ols()
        #output_linear_model = m2.summary()  #works but cant output
        #output=[output_linear_model]

"""effort on the graphing of the model"""
    #x = sm.add_constant()
    #y_hat = fitted.predict(m2)
    #x_pred=np.linspace(m2.min(),m2.max(),50)np.
    #x_pred2=sm.add_constant(x_pred)
    #y_pred=fitted.predict(x_pred2)
    #m2.plot(x_pred,y_pred, '-',color='darkorchid',linewidth=2)
    
























