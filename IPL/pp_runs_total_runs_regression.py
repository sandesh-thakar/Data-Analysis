import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

deliveries = pd.read_csv('Data/deliveries.csv')
matches = pd.read_csv('Data/matches.csv')

matches = matches[matches['season'] >= 2008]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]
deliveries = deliveries[deliveries['inning']<=2]

dataset = []

overs = []

for m in mat:
    mat_deliveries = deliveries[deliveries['match_id']==m]
    inning1 = mat_deliveries[mat_deliveries['inning']==1]
    inning1_overs = inning1['over'].nunique()
    
    if(inning1_overs==20):
        runs = sum(inning1['batsman_runs'])
        pp = inning1[inning1['over']<=6]
        runs_pp = sum(pp['batsman_runs'])
        wickets_pp = sum(~pp['player_dismissed'].isnull())
    
        dataset.append([runs_pp,wickets_pp,runs])
    
    inning2 = mat_deliveries[mat_deliveries['inning']==2]
    inning2_overs = inning2['over'].nunique()
    
    if(inning2_overs==20):
        runs = sum(inning2['batsman_runs'])
        pp = inning2[inning2['over']<=6]
        runs_pp = sum(pp['batsman_runs'])
        wickets_pp = sum(~pp['player_dismissed'].isnull())
        
        dataset.append([runs_pp,wickets_pp,runs])
    
dataset = pd.DataFrame(dataset,columns=['pp_runs','pp_wickets','final_runs'])

X = dataset.iloc[:,0:2]
y = dataset.iloc[:,-1]

#X_train, X_test, y_train, y_test = \
#train_test_split(X, y, test_size=0.5, random_state=0)

regressor = LinearRegression()
regressor.fit(X,y)

print(regressor.coef_,regressor.intercept_)




