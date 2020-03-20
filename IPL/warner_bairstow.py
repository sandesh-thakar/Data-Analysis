import pandas as pd

matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

matches_2019 = matches[matches['season'] == 2019]

mat = []

for i in range(len(matches_2019)):
    mat.append(matches_2019.iloc[i,0])
    
data_2019 = deliveries[deliveries['match_id'].isin(mat)]