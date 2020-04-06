import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('Data/deliveries.csv')
matches = pd.read_csv('Data/matches.csv')

matches = matches[matches['season'] == 2018]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]

deliveries = deliveries[deliveries['inning']<=2]
deliveries = deliveries[deliveries['wide_runs']==0]

batsmen = set()
batsman_data = []

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])

for bat in batsmen:
    bat_deliveries = deliveries[deliveries['batsman']==bat]
    
    balls = len(bat_deliveries)
    fours = 0
    sixes = 0

    for i in range(len(bat_deliveries)):
        get_runs = bat_deliveries.iloc[i,15] - bat_deliveries.iloc[i,16]
        if(get_runs==4):
            fours+=1
        if(get_runs==6):
            sixes+=1
    
    if(fours>0 and sixes>0):
        batsman_data.append([bat,balls,fours,sixes,fours+sixes, \
                             balls/fours,balls/sixes,balls/(fours+sixes)])

batsman_data = pd.DataFrame(batsman_data,columns=['batsman','balls','fours',\
                                                  'sixes','total','bpf','bps','bpb'])

batsman_data = batsman_data[batsman_data['sixes']>=10]

batsman_data.sort_values('bps', axis = 0, ascending = True, \
                 inplace = True, na_position ='last') 

x_data = [batsman_data.iloc[i,6] for i in range(9,-1,-1)]
y_data = [batsman_data.iloc[i,0] for i in range(9,-1,-1)]
y_pos = np.arange(len(y_data))


# Create horizontal bars
plt.barh(y_pos, x_data,color='#164494')
 
plt.title('Balls per Six in IPL 2019(min 10 sixes)')

# Create names on the y-axis
plt.yticks(y_pos, y_data)
 
# Show graphic
plt.show()

