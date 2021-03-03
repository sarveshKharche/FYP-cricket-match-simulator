import pandas as pd
dataset = pd.read_csv('FYP_final_dataset.csv')
dataset= dataset.drop(['Unnamed: 0', 'match_id', 'season', 'team1', 'team2', 'winner',
       'result', 'inning', 'batting_team', 'bowling_team',
       'batsman', 'non_striker',
       'bowler',
       'wide_runs', 'bye_runs', 'legbye_runs',
       'noball_runs', 'penalty_runs', 'batsman_runs', 'extra_runs',
       'dl_applied'],axis=1)
from sklearn.model_selection import train_test_split

X = dataset[['over', 'ball','is_super_over',
       'batsman strike rate', 'batsman average',
       'bowler strike rate', 'bowler average',
       'bowler economy rate']]
y = dataset[['total_runs','player_dismissed']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=100,n_jobs=1)

clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)

print("Complete")
