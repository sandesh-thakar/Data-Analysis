import pandas as pd 

deliveries = pd.read_csv('Data/deliveries.csv')
matches = pd.read_csv('Data/matches.csv')

matches = matches[matches['season'] >= 2008]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]
deliveries = deliveries[deliveries['inning']<=2]

batsmen = ['KD Karthik']
bowlers = ['JJ Bumrah']

deliveries = deliveries[deliveries['batsman'].isin(batsmen)]
deliveries = deliveries[deliveries['bowler'].isin(bowlers)]

pairs = set() 

for i in range(len(deliveries)):
    pairs.add((deliveries.iloc[i,6],deliveries.iloc[i,8]))

pairs = list(pairs)

data = []

for pair in pairs:
    batsman = pair[0]
    bowler = pair[1]
    
    pair_data = deliveries[deliveries['batsman']==batsman]
    pair_data = pair_data[pair_data['bowler']==bowler]
    
    kinds = ['run out','retired hurt','obstructing the field']
    
    runs = 0
    for i in range(len(pair_data)):
        if(pair_data.iloc[i,13]>=1):
            runs+=pair_data.iloc[i,15]
        else:
            runs+=max(0,pair_data.iloc[i,15]-pair_data.iloc[i,16])
    
    balls = len(pair_data[pair_data['wide_runs']==0])
    
    dismissals = pair_data[pair_data['player_dismissed']==batsman]
    dismissals = len(dismissals[~dismissals['dismissal_kind'].isin(kinds)])
    
    
    data.append([pair,runs,balls,dismissals])
    
data = pd.DataFrame(data,columns=['pair','runs','balls','dismissals'])
    
    