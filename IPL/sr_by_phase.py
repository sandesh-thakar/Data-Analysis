import pandas as pd

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches_2019 = matches[matches['season'] == 2019]

mat_19 = []

for i in range(len(matches_2019)):
    mat_19.append(matches_2019.iloc[i,0])

deliveries_2019 = deliveries[deliveries['match_id'].isin(mat_19)]

batsman = 'KL Rahul'

batsman_data = deliveries_2019[deliveries_2019['batsman'] == batsman]
batsman_data = batsman_data[batsman_data['wide_runs'] == 0]

runs = dict()
runs["pp"] = 0
runs["middle"] = 0
runs["death"] = 0

balls = dict()
balls["pp"] = 0
balls["middle"] = 0
balls["death"] = 0

for i in range(0,len(batsman_data)):
    get_over = batsman_data.iloc[i,4]
    get_runs = (batsman_data.iloc[i,15] - batsman_data.iloc[i,16])
    
    if(get_over<=6):
        runs["pp"] += get_runs
        balls["pp"] += 1
    elif(get_over<=15):
        runs["middle"] += get_runs
        balls["middle"] += 1
    else:
        runs["death"] += get_runs
        balls["death"] += 1
        
print("Powerplay SR: ",runs["pp"]*100/balls["pp"])
print("Middle Overs SR: ",runs["middle"]*100/balls["middle"])
print("Death Overs SR: ",runs["death"]*100/balls["death"])