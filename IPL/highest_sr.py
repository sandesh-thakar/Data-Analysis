import pandas as pd

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches_2019 = matches[matches['season'] >= 2019]

mat_19 = []

for i in range(len(matches_2019)):
    mat_19.append(matches_2019.iloc[i,0])

deliveries = deliveries[deliveries['match_id'].isin(mat_19)]
deliveries = deliveries[deliveries['wide_runs']==0]

batsmen = set()

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])
    
batsmen = list(batsmen)

batsman_data = dict()

for bat in batsmen:
    batsman_data[bat] = dict()
    batsman_data[bat]["runs_pp"] = 0
    batsman_data[bat]["runs_mid"] = 0
    batsman_data[bat]["runs_do"] = 0
    batsman_data[bat]["balls_pp"] = 0
    batsman_data[bat]["balls_mid"] = 0
    batsman_data[bat]["balls_do"] = 0
    
for i in range(len(deliveries)):
    get_over = deliveries.iloc[i,4]
    get_batsman = deliveries.iloc[i,6]
    get_runs = deliveries.iloc[i,15] - deliveries.iloc[i,16]
    
    if(get_over<=6):
        batsman_data[get_batsman]['runs_pp'] += get_runs
        batsman_data[get_batsman]['balls_pp'] += 1
    elif(get_over>=7 and get_over<=15):
        batsman_data[get_batsman]['runs_mid'] += get_runs
        batsman_data[get_batsman]['balls_mid'] += 1
    else:
        batsman_data[get_batsman]['runs_do'] += get_runs
        batsman_data[get_batsman]['balls_do'] += 1
        
data = []

for bat in batsman_data.keys():
    runs_pp = batsman_data[bat]['runs_pp']
    balls_pp = batsman_data[bat]['balls_pp']
    runs_mid = batsman_data[bat]['runs_mid']
    balls_mid = batsman_data[bat]['balls_mid']
    runs_do = batsman_data[bat]['runs_do']
    balls_do = batsman_data[bat]['balls_do']
    runs = runs_pp + runs_mid + runs_do
    balls = balls_pp + balls_mid + balls_do
    data.append([bat,runs,balls,runs_pp,balls_pp,runs_mid,balls_mid,runs_do,balls_do])
    
data=pd.DataFrame(data,columns=['batsman','runs','balls','runs_pp','balls_pp','runs_mid', \
                                'balls_mid','runs_do','balls_do'])

powerplay_sr = []

for i in range(len(data)):
    if(data.iloc[i,4]!=0):
        powerplay_sr.append([data.iloc[i,0],data.iloc[i,3],data.iloc[i,4], \
                             data.iloc[i,3]*100/data.iloc[i,4]])
        
powerplay_sr = pd.DataFrame(powerplay_sr,columns=['batsman','pp_runs','pp_balls','pp_sr'])

powerplay_sr = powerplay_sr[powerplay_sr['pp_balls']>=200]



middle_sr = []

for i in range(len(data)):
    if(data.iloc[i,6]!=0):
        middle_sr.append([data.iloc[i,0],data.iloc[i,5],data.iloc[i,6], \
                             data.iloc[i,5]*100/data.iloc[i,6]])
        
middle_sr = pd.DataFrame(middle_sr,columns=['batsman','middle_runs','middle_balls','middle_sr'])

middle_sr = middle_sr[middle_sr['middle_balls']>=200]




death_sr = []

for i in range(len(data)):
    if(data.iloc[i,8]!=0):
        death_sr.append([data.iloc[i,0],data.iloc[i,7],data.iloc[i,8], \
                             data.iloc[i,7]*100/data.iloc[i,8]])
        
death_sr = pd.DataFrame(death_sr,columns=['batsman','do_runs','do_balls','do_sr'])

death_sr = death_sr[death_sr['do_balls']>=60]
