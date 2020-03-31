import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

matches = pd.read_csv('matches.csv')
matches = matches[matches['season']>=2015]
matches = matches[matches['result']!='no result']

toss_wins = dict()
bat = dict()
field = dict()
total = dict()

for i in range(len(matches)):
    matches.iloc[i,4] = matches.iloc[i,4].split()[0]
    matches.iloc[i,5] = matches.iloc[i,5].split()[0]
    matches.iloc[i,6] = matches.iloc[i,6].split()[0]
    matches.iloc[i,10] = matches.iloc[i,10].split()[0]
        

for i in range(len(matches)):
    toss_winner = matches.iloc[i,6]
    
    if(toss_winner not in toss_wins.keys()):
        toss_wins[toss_winner] = 0
    toss_wins[toss_winner] += 1
    
    team1=matches.iloc[i,4]
    team2=matches.iloc[i,5]
    
    if(toss_winner==team1):
        toss_loser=team2
    else:
        toss_loser=team1    
    
    
    if(matches.iloc[i,7]=='bat'):
        if(toss_winner not in bat.keys()):
            bat[toss_winner] = 0
        bat[toss_winner] += 1
        chasing = toss_loser
        defending = toss_winner
    else:
        if(toss_winner not in field.keys()):
            field[toss_winner] = 0
        field[toss_winner] += 1
        chasing = toss_winner
        defending = toss_loser
    
    if(team1 not in total.keys()):
        total[team1]=0
    if(team2 not in total.keys()):
        total[team2]=0
        
    total[team1] += 1
    total[team2] += 1

toss_data = []
    
for key in total.keys():
    toss_data.append([key,total[key],toss_wins[key],bat[key],field[key],\
                      field[key]*100/toss_wins[key]])
    
toss_data = pd.DataFrame(toss_data,columns=['team','matches',\
                                            'toss_wins','bat','field','chase_percentage'])

toss_w = 0
toss_l = 0

for i in range(len(matches)):
    if(matches.iloc[i,6]==matches.iloc[i,10]):
        toss_w += 1
    else:
        toss_l += 1

