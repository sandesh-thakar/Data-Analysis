import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches_2019 = matches[matches['season'] >= 2018]

mat_19 = []

for i in range(len(matches_2019)):
    mat_19.append(matches_2019.iloc[i,0])

deliveries_2019 = deliveries[deliveries['match_id'].isin(mat_19)]

deliveries_2019_pp = deliveries_2019[deliveries_2019['over']<=6]

bowlers = set()
for i in range(len(deliveries_2019_pp)):
    bowlers.add(deliveries_2019_pp.iloc[i,8])
bowlers = list(bowlers)   

bowlers_data = dict()

for bowl in bowlers:
    bowlers_data[bowl] = dict()
    bowlers_data[bowl]['dots'] = 0
    bowlers_data[bowl]['balls'] = 0
    bowlers_data[bowl]['wickets'] = 0
    
for i in range(len(deliveries_2019_pp)):
    get_bowler = deliveries_2019_pp.iloc[i,8]
    get_bowler_runs = deliveries_2019_pp.iloc[i,15] - \
    deliveries_2019_pp.iloc[i,12] - deliveries_2019_pp.iloc[i,11]
    if(get_bowler_runs == 0):
        bowlers_data[get_bowler]['dots'] += 1
    bowlers_data[get_bowler]['balls'] += 1
    if(type(deliveries_2019_pp.iloc[i,18])==str):
        bowlers_data[get_bowler]['wickets'] += 1
    
bowlers_pp = []

for bowl in bowlers:
    if(bowlers_data[bowl]['dots']!=0 and bowlers_data[bowl]['wickets']!=0):
        bowlers_pp.append([bowl,bowlers_data[bowl]['wickets'],bowlers_data[bowl]['dots'], \
                                bowlers_data[bowl]['balls'], \
                            bowlers_data[bowl]['balls']/bowlers_data[bowl]['dots'],\
                            bowlers_data[bowl]['balls']/bowlers_data[bowl]['wickets']])
    
bowlers_pp = pd.DataFrame(bowlers_pp,columns=['bowler','wickets','dots', \
                                                        'balls','balls_per_dot','sr'])
        
bowlers_pp = bowlers_pp[bowlers_pp['balls']>=200]
    
bowlers_pp.sort_values('sr', axis = 0, ascending = True, \
                 inplace = True, na_position ='last') 

x_data = [bowlers_pp.iloc[i,5] for i in range(10,-1,-1)]
y_data = [bowlers_pp.iloc[i,0] for i in range(10,-1,-1)]
y_pos = np.arange(len(y_data))

colors = ['blue','red','yellow','dark blue','black','pink','yellow','violet','orange','blue','pink']

# Create horizontal bars
plt.barh(y_pos, x_data,color=colors)
 

plt.title("Powerplay SR since 2018 (min 200 balls)")

# Create names on the y-axis
plt.yticks(y_pos, y_data)
 
# Show graphic
plt.show()

