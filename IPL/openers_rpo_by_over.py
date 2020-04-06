import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('Data/deliveries.csv')
matches = pd.read_csv('Data/matches.csv')

matches = matches[matches['season'] == 2019]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]
deliveries = deliveries[deliveries['wide_runs']==0]
deliveries = deliveries[deliveries['inning']<=2]

openers = ['DA Warner','KL Rahul','Q de Kock']

opener_runs = dict()
opener_balls = dict()
opener_rpo = dict()

for bat in openers:
    opener_runs[bat] = dict()
    opener_balls[bat] = dict()
    opener_rpo[bat] =dict()
    for over in range(1,21):
        opener_runs[bat][over] = 0
        opener_balls[bat][over] = 0
        opener_rpo[bat][over] = 0
        
for bat in openers:
    bat_deliveries = deliveries[deliveries['batsman']==bat]
    for over in range(1,21):
        over_deliveries = bat_deliveries[bat_deliveries['over']==over]
        opener_balls[bat][over] = len(over_deliveries)
        for i in range(len(over_deliveries)):
            opener_runs[bat][over] += over_deliveries.iloc[i,15] - over_deliveries.iloc[i,16]
        if(opener_balls[bat][over]!=0):
            opener_rpo[bat][over] = opener_runs[bat][over]*6.0/opener_balls[bat][over]

plt.figure(figsize=(19.20,10.80))
plt.xticks(np.arange(21))
        
for bat in openers:
    x = [over for over in range(1,21)]
    y = [opener_rpo[bat][over] for over in range(1,21)]
    plt.plot(x,y,label=bat)

plt.legend()