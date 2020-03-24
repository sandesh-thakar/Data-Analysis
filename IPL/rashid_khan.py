import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches = matches[matches['season'] >= 2017]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])

deliveries = deliveries[deliveries['match_id'].isin(mat)]

deliveries = deliveries[deliveries['bowler'] == 'Rashid Khan']
deliveries = deliveries[deliveries['inning'] <= 2]

over = dict()

for i in range(1,21):
    over[i] = dict()
    over[i]['runs'] = 0
    over[i]['balls'] = 0
    over[i]['wickets'] = 0
    over[i]['boundaries'] = 0

for i in range(len(deliveries)):
    get_over = deliveries.iloc[i,4]
    get_wide_nb = deliveries.iloc[i,10] + deliveries.iloc[i,13]
    if(get_wide_nb == 0):
        over[get_over]['balls'] += 1
    if(type(deliveries.iloc[i,18])==str and deliveries.iloc[i,19]!='run out'):
        over[get_over]['wickets'] += 1
    get_bowler_runs = deliveries.iloc[i,15] - deliveries.iloc[i,12] - deliveries.iloc[i,11]
    over[get_over]['runs'] += get_bowler_runs
    if(get_bowler_runs>=4):
        over[get_over]['boundaries'] += 1
    
overs_data = []

 
for i in range(1,21):
    try:
        overs_data.append([i,over[i]['balls'],over[i]['runs'],over[i]['wickets'], \
                               over[i]['boundaries'],over[i]['runs']*6.0/over[i]['balls']])
    except ZeroDivisionError:
        overs_data.append([i,over[i]['balls'],over[i]['runs'],over[i]['wickets'], \
                               over[i]['boundaries'],0])
        
overs_data = pd.DataFrame(overs_data,columns=['over','balls','runs','wickets' \
                                                      ,'boundaries','er'])
    

over_no = [i for i in range(1,21)]
y_pos = np.arange(len(over_no))
over_wickets = [over[i]['wickets'] for i in range(1,21)]

plt.bar(y_pos, over_wickets, align='center', alpha=0.5)
plt.xticks(y_pos, over_no)
plt.ylabel('Wickets')
plt.title('Rashid Khan Wickets by Over')

plt.show()
