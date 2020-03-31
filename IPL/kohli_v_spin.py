import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches = matches[matches['season'] >= 2017]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])

top_5 = ['Rashid Khan']

deliveries = deliveries[deliveries['match_id'].isin(mat)]

deliveries = deliveries[deliveries['wide_runs']==0]
deliveries = deliveries[deliveries['bowler'].isin(top_5)]

batsmen = set()

for i in range(len(deliveries)):
    batsmen.add(deliveries.iloc[i,6])

batsmen = list(batsmen)

batsman_data = []

for bat in batsmen:
    bat_deliveries = deliveries
    bat_deliveries = bat_deliveries[bat_deliveries['batsman']==bat]
    
    runs = 0
    dismissals = 0

    for i in range(len(bat_deliveries)):
        runs += bat_deliveries.iloc[i,15] - bat_deliveries.iloc[i,16]
        if(type(bat_deliveries.iloc[i,18])==str and bat_deliveries.iloc[i,19]!='run out'):
            dismissals += 1
        
    batsman_data.append([bat,runs,len(bat_deliveries),dismissals, \
                         runs*100/len(bat_deliveries)])

batsman_data = pd.DataFrame(batsman_data,columns=['batsman','runs','balls', \
                                                  'dismissals','sr'])

batsman_data = batsman_data[batsman_data['balls']>=18]
    
batsman_data.sort_values('sr', axis = 0, ascending = False, \
                 inplace = True, na_position ='last') 


x_data = [batsman_data.iloc[i,4] for i in range(10,-1,-1)]
y_data = [batsman_data.iloc[i,0] for i in range(10,-1,-1)]
y_pos = np.arange(len(y_data))


# Create horizontal bars
plt.barh(y_pos, x_data)
 
plt.title('Strike rate against Bumrah since IPL 2017 (min 18 balls)')

# Create names on the y-axis
plt.yticks(y_pos, y_data)
 
# Show graphic
plt.show()
