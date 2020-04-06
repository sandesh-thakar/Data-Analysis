import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def fitRegressor():
    deliveries = pd.read_csv('Data/deliveries.csv')
    matches = pd.read_csv('Data/matches.csv')
    
    matches = matches[matches['season'] >= 2015]
    matches = matches[matches['season'] <= 2018]
    
    mat = []
    
    for i in range(len(matches)):
        mat.append(matches.iloc[i,0])
        
    deliveries = deliveries[deliveries['match_id'].isin(mat)]
    deliveries = deliveries[deliveries['inning']<=2]
    
    dataset = []
    
    for m in mat:
        mat_deliveries = deliveries[deliveries['match_id']==m]
        inning1 = mat_deliveries[mat_deliveries['inning']==1]
        inning1_overs = inning1['over'].nunique()
        
        if(inning1_overs==20):
            runs = sum(inning1['batsman_runs'])
            
            pp = inning1[inning1['over']<=6]
            runs_pp = sum(pp['batsman_runs'])
            wickets_pp = sum(~pp['player_dismissed'].isnull())
            
            mid = inning1[inning1['over']>=7]
            mid = mid[mid['over']<=12]
            runs_mid = sum(mid['batsman_runs'])
            wickets_mid = sum(~mid['player_dismissed'].isnull())
            
            dataset.append([runs_pp,wickets_pp,runs_mid,wickets_mid,runs])
        
        inning2 = mat_deliveries[mat_deliveries['inning']==2]
        inning2_overs = inning2['over'].nunique()
        
        if(inning2_overs==20):
            runs = sum(inning2['batsman_runs'])
            
            pp = inning2[inning2['over']<=6]
            runs_pp = sum(pp['batsman_runs'])
            wickets_pp = sum(~pp['player_dismissed'].isnull())
            
            mid = inning2[inning2['over']>=7]
            mid = mid[mid['over']<=12]
            runs_mid = sum(mid['batsman_runs'])
            wickets_mid = sum(~mid['player_dismissed'].isnull())
            
            dataset.append([runs_pp,wickets_pp,runs_mid,wickets_mid,runs])
        
    dataset = pd.DataFrame(dataset,columns=['pp_runs','pp_wickets','mid_runs',\
                                            'mid_wickets','final_runs'])
    
    X = dataset.iloc[:,0:4]
    y = dataset.iloc[:,-1]
    
    #X_train, X_test, y_train, y_test = \
    #train_test_split(X, y, test_size=0.5, random_state=0)
    
    regressor = LinearRegression()
    regressor.fit(X,y)


    return regressor

def getTestData():
    deliveries = pd.read_csv('Data/deliveries.csv')
    matches = pd.read_csv('Data/matches.csv')
    
    matches = matches[matches['season'] == 2019]
    
    mat = []
    
    for i in range(len(matches)):
        mat.append(matches.iloc[i,0])
        
    deliveries = deliveries[deliveries['match_id'].isin(mat)]
    deliveries = deliveries[deliveries['inning']<=2]
    
    dataset = []
    
    for m in mat:
        mat_deliveries = deliveries[deliveries['match_id']==m]
        inning1 = mat_deliveries[mat_deliveries['inning']==1]
        inning1_overs = inning1['over'].nunique()
        
        if(inning1_overs==20):
            runs = sum(inning1['batsman_runs'])
            
            pp = inning1[inning1['over']<=6]
            runs_pp = sum(pp['batsman_runs'])
            wickets_pp = sum(~pp['player_dismissed'].isnull())
            
            mid = inning1[inning1['over']>=7]
            mid = mid[mid['over']<=12]
            runs_mid = sum(mid['batsman_runs'])
            wickets_mid = sum(~mid['player_dismissed'].isnull())
            
            dataset.append([runs_pp,wickets_pp,runs_mid,wickets_mid,runs])
        
        inning2 = mat_deliveries[mat_deliveries['inning']==2]
        inning2_overs = inning2['over'].nunique()
        
        if(inning2_overs==20):
            runs = sum(inning2['batsman_runs'])
            
            pp = inning2[inning2['over']<=6]
            runs_pp = sum(pp['batsman_runs'])
            wickets_pp = sum(~pp['player_dismissed'].isnull())
            
            mid = inning2[inning2['over']>=7]
            mid = mid[mid['over']<=12]
            runs_mid = sum(mid['batsman_runs'])
            wickets_mid = sum(~mid['player_dismissed'].isnull())
            
            dataset.append([runs_pp,wickets_pp,runs_mid,wickets_mid,runs])
        
    dataset = pd.DataFrame(dataset,columns=['pp_runs','pp_wickets','mid_runs',\
                                            'mid_wickets','final_runs'])
    
    X = dataset.iloc[:,0:4]
    y = dataset.iloc[:,-1]
    
    return X,y

regressor = fitRegressor()
X,y = getTestData()
y_actual = list(y)
y_pred = list(regressor.predict(X))

rmse = 0

for i in range(len(y_actual)):
    rmse += (y_actual[i]-y_pred[i])**2
    
rmse = (rmse/len(y_actual))**0.5

matches = pd.read_csv('Data/matches.csv')

prediction_data = []

for i in range(len(X)):
    mat = matches[matches['id']==X.iloc[i,0]]
    prediction_data.append([mat.iloc[0,4],mat.iloc[0,5],\
                            round(y_pred[i]),y_actual[i],-round(y_pred[i])+y_actual[i]])
    
prediction_data = pd.DataFrame(prediction_data,columns=['team1','team2',\
                                                        'predicted_total',\
                                                        'actual_total','difference'])
