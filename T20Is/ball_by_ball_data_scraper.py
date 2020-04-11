import json
import requests
import pandas as pd
import math


data = []
cols = []
cols.append('match_id')
cols.append('inning')
cols.append('batting_team')
cols.append('bowling_team')
cols.append('over')
cols.append('ball')
cols.append('batsman')
cols.append('bowler')
cols.append('wide_runs')
cols.append('bye_runs')
cols.append('legbye_runs')
cols.append('noball_runs')
cols.append('total_runs')
cols.append('extra_runs')
cols.append('player_dismissed')
cols.append('dismissal_kind')

series = 18610

mat = [1141232]

for match_id in mat:
    for inning in range(1,3):
        balls=[]
        for i in range(1,9):
            try:
                URL = "https://site.web.api.espn.com/apis/site/v2/sports/cricket/"+str(series)+"/playbyplay?contentorigin=espn&event="+str(match_id)+"&page="+str(i)+"&period="+str(inning)+"&section=cricinfo"
            except Exception as e:
                print(i,e)
                continue
            try:
                response = requests.get(URL) 
                print(match_id,inning,i,response)
                response_dict = json.loads(response.text)
                items = response_dict['commentary']['items']
            except Exception as e:
                print(i,e)
                continue
        
            for item in items:
                balls.append(item)
        
        print(len(balls))
        
        for ball in balls:
            try:
                temp = []
                
                temp.append(match_id)
                temp.append(inning)
                temp.append(ball['batsman']['team']['name'])
                temp.append(ball['bowler']['team']['name'])
                temp.append(int(str(ball['over']['actual']).split('.')[0])+1)
                temp.append(ball['over']['ball'])
                temp.append(ball['batsman']['athlete']['name'])
                temp.append(ball['bowler']['athlete']['name'])
                temp.append(ball['over']['wide'])
                temp.append(ball['over']['byes'])
                temp.append(ball['over']['legByes'])
                temp.append(ball['over']['noBall'])
                
                val = ball['scoreValue']
                
                extras = ball['over']['wide']+ball['over']['byes']+\
                ball['over']['legByes']+ball['over']['noBall']
                
                if(extras>val):
                    val=extras
                
                temp.append(val)
                temp.append(extras)
                
                if(ball['dismissal']['dismissal']==True):
                    temp.append(ball['dismissal']['batsman']['athlete']['name'])
                else:
                    temp.append(math.nan)
                temp.append(ball['dismissal']['type'])
                
                if(ball['dismissal']['type']=='run out'):
                    if(ball['otherBatsman']['athlete']['shortName'] in ball['dismissal']['text'].split('(')[0]):
                        temp[14]=ball['otherBatsman']['athlete']['name']
                
                data.append(temp)
            except Exception as e:
                print(match_id,inning,ball['id'],e)

data = pd.DataFrame(data,columns=cols)    
data = data[data['batsman']=='Dinesh Karthik']

for bat in list(data['batsman'].unique()):
    bat_data = data[data['batsman']==bat]
    bat_data = bat_data[bat_data['wide_runs']==0]
    print(bat,sum(bat_data['total_runs']-bat_data['extra_runs']),len(bat_data))

path = "IndiaT20Is/2018/"+str(series)+".csv"
data.to_csv(path)
