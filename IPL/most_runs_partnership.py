import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches = matches[matches['season'] >= 2018]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]
deliveries = deliveries[deliveries['inning']<=2]

batsmen = set()

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])

batsmen = list(batsmen)

batsman_data = []

for bat in batsmen:
    strike_data = deliveries[deliveries['batsman']==bat]
    non_strike_data = deliveries[deliveries['non_striker']==bat]
    
    strike_runs = 0
    for i in range(len(strike_data)):
        strike_runs += strike_data.iloc[i,15]
        
    non_strike_runs = 0
    for i in range(len(non_strike_data)):
        non_strike_runs += non_strike_data.iloc[i,15]
        
    batsman_data.append([bat,strike_runs,non_strike_runs,\
                         strike_runs+non_strike_runs])

batsman_data = pd.DataFrame(batsman_data,columns=['batsman','stike_runs',\
                                                  'non_strike_runs','total_runs'])     
    
batsman_data.sort_values('total_runs', axis = 0, ascending = False, \
                 inplace = True, na_position ='last') 
    
players = [batsman_data.iloc[i,0] for i in range(9,-1,-1)]
y_pos = np.arange(len(players))
strike = [batsman_data.iloc[i,1] for i in range(9,-1,-1)]
non_strike = [batsman_data.iloc[i,2] for i in range(9,-1,-1)]

plt.barh(y_pos, strike, align='center', color='#2516c7', label='Strike')
plt.barh(y_pos, non_strike, left=strike,align='center',color='#786ee0', label='Non-Strike')
plt.yticks(y_pos, players)
plt.title('Most partnership runs since IPL 2018',font=25) 
plt.legend()