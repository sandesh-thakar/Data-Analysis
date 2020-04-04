import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')

matches = matches[matches['season'] >= 2017]

mat = []

for i in range(len(matches)):
    mat.append(matches.iloc[i,0])
    
deliveries = deliveries[deliveries['match_id'].isin(mat)]
deliveries = deliveries[deliveries['inning']<=2]

lh = pd.read_csv('left_handers.csv')
rh = pd.read_csv('right_handers.csv')
spin = pd.read_csv('spin.csv')
lh = [lh.iloc[i,1] for i in range(len(lh))]
rh = [rh.iloc[i,1] for i in range(len(rh))]
spin = [spin.iloc[i,1] for i in range(len(spin))]

deliveries = deliveries[deliveries['batsman'].isin(lh)]
deliveries = deliveries[deliveries['bowler'].isin(spin)]
#deliveries = deliveries[deliveries['wide_runs']==0]
#deliveries = deliveries[deliveries['noball_runs']==0]

runs = {'os': 0, 'ls': 0, 'slo': 0, 'slu': 0}
balls = {'os': 0, 'ls': 0, 'slo': 0, 'slu': 0}

spin_type = pd.read_csv('spin_type.csv')

style = dict()

for i in range(len(spin_type)):
    style[spin_type.iloc[i,0]] = spin_type.iloc[i,1]

for i in range(len(deliveries)):
    get_bowler = deliveries.iloc[i,8]
    get_runs = deliveries.iloc[i,15] - deliveries.iloc[i,12] - \
    deliveries.iloc[i,11]
    get_widenb = deliveries.iloc[i,10] + deliveries.iloc[i,13]
    
    if get_widenb == 0:
        balls[style[get_bowler]] += 1
    runs[style[get_bowler]] += get_runs
    
deliveries = deliveries[~deliveries['player_dismissed'].isnull()]
deliveries = deliveries[deliveries['dismissal_kind']!='run out']

bowlers = [style[deliveries.iloc[i,8]] for i in range(len(deliveries))]

wickets = {'os': 0, 'ls': 0, 'slo': 0, 'slu': 0}


for bowl in bowlers:
    wickets[bowl] += 1

sr = {key:balls[key]/wickets[key] for key in wickets.keys()}
avg = {key:runs[key]/wickets[key] for key in wickets.keys()}


