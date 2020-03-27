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

bat_dismissals = dict()

for i in range(len(deliveries)):
    bat_dismissed = deliveries.iloc[i,18]
    if bat_dismissed in bat_dismissals.keys():
        bat_dismissals[bat_dismissed] += 1
    else:
        bat_dismissals[bat_dismissed] = 1

deliveries = deliveries[deliveries['wide_runs']==0]

batsmen = set()

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])
    
batsmen = list(batsmen)

batsman_data = []

for bat in batsmen:
    bat_deliveries = deliveries
    bat_deliveries = bat_deliveries[bat_deliveries['batsman']==bat]
    
    runs = 0

    for i in range(len(bat_deliveries)):
        runs += bat_deliveries.iloc[i,15] - bat_deliveries.iloc[i,16]
        
    if(bat in bat_dismissals.keys()):    
        dismissals = bat_dismissals[bat]
    else:
        dismissals = 0
        
    if(dismissals==0):
        batsman_data.append([bat,runs,len(bat_deliveries), \
                             runs*100/len(bat_deliveries),dismissals, \
    0])
    else:
        batsman_data.append([bat,runs,len(bat_deliveries), \
                             runs*100/len(bat_deliveries),dismissals, \
    runs/dismissals])
    
batsman_data = pd.DataFrame(batsman_data,columns=['batsman','runs','balls', \
                                                  'sr','dismissals','avg'])
    
batsman_data = batsman_data[batsman_data['balls']>=300]

batsman_plot = []

plt.figure(figsize=(19.20,10.80))
plt.rc('xtick', labelsize=20) 
plt.rc('ytick', labelsize=20) 

for i in range(len(batsman_data)):
    if(batsman_data.iloc[i,3]>=150):
        batsman_plot.append(batsman_data.iloc[i,0])
    elif(batsman_data.iloc[i,5]>=40):
        batsman_plot.append(batsman_data.iloc[i,0])

for i in range(len(batsman_data)):
    x = batsman_data.iloc[i,3]
    y = batsman_data.iloc[i,5] 
    
    if(batsman_data.iloc[i,0] in batsman_plot):
        name = batsman_data.iloc[i,0].split()[1]
        if name == 'de':
            name = 'de Villiers'
        plt.text(x+0.5, y-0.5, name, fontsize=20,weight='bold')
        plt.scatter(x, y, s=15,color='red')
    else:
        plt.scatter(x, y, s=4.0,color='blue')
        
        
plt.axvline(x=140,linestyle='--',linewidth=1.0,color='black')
plt.axvline(x=150,linestyle='--',linewidth=1.0,color='black')
plt.axvline(x=160,linestyle='--',linewidth=1.0,color='black')
plt.axvline(x=170,linestyle='--',linewidth=1.0,color='black')
plt.axhline(y=35,linestyle='--',linewidth=1.0,color='black')
plt.axhline(y=40,linestyle='--',linewidth=1.0,color='black')
plt.axhline(y=45,linestyle='--',linewidth=1.0,color='black')
plt.axhline(y=50,linestyle='--',linewidth=1.0,color='black')

plt.title('Average vs SR in IPL since 2018(min 300 balls)',fontsize=22.5,weight='bold')
