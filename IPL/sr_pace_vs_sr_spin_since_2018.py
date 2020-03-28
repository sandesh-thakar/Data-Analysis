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
deliveries = deliveries[deliveries['wide_runs']==0]
deliveries = deliveries[deliveries['inning']<=2]

bowlers = set()

for i in range(len(deliveries)):
    bowlers.add(deliveries.iloc[i,8])

bowlers = list(bowlers)

batsmen = set()

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])

batsmen = list(batsmen)

batsman_data = []

for bat in batsmen:
    bat_deliveries = deliveries[deliveries['batsman']==bat]
    spin_data = bat_deliveries[bat_deliveries['bowler'].isin(spin)]
    pace_data = bat_deliveries[bat_deliveries['bowler'].isin(pace)]
    
    dat = []
    dat.append(bat)
    
    runs_spin = 0
    for i in range(len(spin_data)):
        runs_spin += spin_data.iloc[i,15] - spin_data.iloc[i,16]
    dat.append(runs_spin)
    dat.append(len(spin_data))
    
    runs_pace = 0
    for i in range(len(pace_data)):
        runs_pace += pace_data.iloc[i,15] - pace_data.iloc[i,16]
    dat.append(runs_pace)
    dat.append(len(pace_data))
    
    batsman_data.append(dat)
    
batsman_data = pd.DataFrame(batsman_data,columns=['batsman','spin_runs', \
                                                  'spin_balls','pace_runs',\
                                                  'pace_balls'])    

batsman_data = batsman_data[batsman_data['spin_runs']>=200] 
batsman_data = batsman_data[batsman_data['pace_runs']>=200]   


plt.figure(figsize=(19.20,10.80))
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 

for i in range(len(batsman_data)):
    name = batsman_data.iloc[i,0]
    x = batsman_data.iloc[i,1]*100/batsman_data.iloc[i,2]
    y = batsman_data.iloc[i,3]*100/batsman_data.iloc[i,4]
    if(x>=150 or y>=150):
        plt.scatter(x,y,s=20,color='red')
        plt.text(x+0.5, y-0.5, name, fontsize=20,weight='bold')
    else:
        plt.scatter(x,y,s=5,color='blue')

plt.xlabel('Spin',fontsize=15)    
plt.ylabel('Pace',fontsize=15)    
    
plt.axvline(x=150,linestyle='--',linewidth=1.0,color='black')
plt.axhline(y=150,linestyle='--',linewidth=1.0,color='black')

plt.title('Pace SR v Spin SR in IPL since 2018(min 200 runs against both)',fontsize=22.5,weight='bold')