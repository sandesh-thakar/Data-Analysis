from flask import Flask, request, render_template
import pandas as pd
import os      

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

data = os.path.join(THIS_FOLDER, 'deliveries.csv')
data = pd.read_csv(data)
matches = os.path.join(THIS_FOLDER, 'matches.csv')
matches = pd.read_csv(matches)

batsmen_file = os.path.join(THIS_FOLDER, 'batsmen.txt')
batsmen = []
with open(batsmen_file, "r") as f:
  for line in f:
    batsmen.append(str(line.strip()))
batsmen.sort()

bowlers_file = os.path.join(THIS_FOLDER, 'bowlers.txt')
bowlers = []
with open(bowlers_file, "r") as f:
  for line in f:
    bowlers.append(str(line.strip()))
bowlers.sort()

seasons = [s for s in range(2008,2020)]
kinds = ['run out','retired hurt','obstructing the field']

app = Flask(__name__)
	
@app.route("/", methods=["GET", "POST"])
def home():
	runs = balls = dismissals = sr = avg = 0
	batsman = ""
	bowler = ""

	if request.method=="POST":
		runs = balls = dismissals = sr = avg = 0
		batsman = ''
		bowler = ''
		batsman = str(request.form["batsman"])
		bowler = str(request.form["bowler"])

		flag = 1
		try:
			fr = int(request.form["from"])
			to = int(request.form["to"])
			if(not(fr<=to and fr>=2008 and to<=2019)):
				flag = 0
		except:
			fr = 2008
			to = 2019
			flag = 0

		if(len(batsman.strip())==0 or len(bowler.strip())==0):
			batsman=bowler=""

		temp_matches = matches[matches['season']>=fr]
		temp_matches = temp_matches[temp_matches['season']<=to]

		mat = []
		for i in range(len(temp_matches)):
			mat.append(temp_matches.iloc[i,0])

		h2h = data[data['batsman']==batsman]
		h2h = h2h[h2h['bowler']==bowler]
		h2h = h2h[h2h['match_id'].isin(mat)]
		h2h = h2h[h2h['wide_runs']==0]

		if(not((batsman in batsmen) and(bowler in bowlers))):
			flag=0
			batsman=bowler=""
			fr=2008
			to=2019

		if(len(h2h)!=0 and flag==1):
			runs = sum(h2h['batsman_runs']-h2h['extra_runs'])
			balls = len(h2h)
			dismissals = h2h[h2h['player_dismissed']==batsman]
			dismissals = len(dismissals[~dismissals['dismissal_kind'].isin(kinds)])
			sr = 0
			if(balls!=0):
				sr=round(runs*100/balls,2)
			avg = runs
			if(dismissals!=0):
				avg=round(runs/dismissals,2)
		else:
			runs=balls=dismissals=sr=avg=0

	if request.method=="POST":
	    return render_template("home.html",batnames=batsmen,bowlnames=bowlers,years=seasons,\
	    	batsman=batsman,bowler=bowler,runs=runs,balls=balls,\
	    	dismissals=dismissals,sr=sr,avg=avg,lastBat=batsman,lastBowl=bowler,lastFor=fr,lastTo=to)
	
	return render_template("home_load.html",batnames=batsmen,bowlnames=bowlers,years=seasons)
	

if __name__ == "__main__":
    app.run(debug=True)