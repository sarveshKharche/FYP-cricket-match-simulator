from django.http import HttpResponse
from django.shortcuts import render


import joblib as jb
import pandas as pd
import numpy as np

def home(request):
    return render(request, "home.html")

def team(request):
    return render(request, "team.html")

def result(request):
    loaded_model_runs = jb.load('final_deploy_runs.sav')
    loaded_model_wickets = jb.load('final_deploy_wickets.sav')

    team1 = []
    team2 = []

    P1o1 = request.GET['P1/1']
    P1o2 = request.GET['P1/2']
    P1o3 = request.GET['P1/3']
    P1o4 = request.GET['P1/4']
    P1o5 = request.GET['P1/5']
    P1o6 = request.GET['P1/6']
    P1o7 = request.GET['P1/7']
    P1o8 = request.GET['P1/8']
    P1o9 = request.GET['P1/9']
    P1o10 = request.GET['P1/10']
    P1o11 = request.GET['P1/11']

    P2o1 = request.GET['P2/1']
    P2o2 = request.GET['P2/2']
    P2o3 = request.GET['P2/3']
    P2o4 = request.GET['P2/4']
    P2o5 = request.GET['P2/5']
    P2o6 = request.GET['P2/6']
    P2o7 = request.GET['P2/7']
    P2o8 = request.GET['P2/8']
    P2o9 = request.GET['P2/9']
    P2o10 = request.GET['P2/10']
    P2o11 = request.GET['P2/11']


    team1.append(P1o1)
    team1.append(P1o2)
    team1.append(P1o3)
    team1.append(P1o4)
    team1.append(P1o5)
    team1.append(P1o6)
    team1.append(P1o7)
    team1.append(P1o8)
    team1.append(P1o9)
    team1.append(P1o10)
    team1.append(P1o11)

    team2.append(P2o1)
    team2.append(P2o2)
    team2.append(P2o3)
    team2.append(P2o4)
    team2.append(P2o5)
    team2.append(P2o6)
    team2.append(P2o7)
    team2.append(P2o8)
    team2.append(P2o9)
    team2.append(P2o10)
    team2.append(P2o11)


    playerData_with_clusters = pd.read_csv('PlayerData_clusters.csv')

    batClustT1={}
    bowlClustT1={}
    batClustT2={}
    bowlClustT2={}
    
    for i in range(11):
        for j in range(playerData_with_clusters.shape[0]):
            if team1[i]==playerData_with_clusters['Player'][j]:
                batClustT1[team1[i]]=playerData_with_clusters['Batting Cluster'][j]
                bowlClustT1[team1[i]]=playerData_with_clusters['Bowling Cluster'][j]
            if team2[i]==playerData_with_clusters['Player'][j]:
                batClustT2[team2[i]]=playerData_with_clusters['Batting Cluster'][j]
                bowlClustT2[team2[i]]=playerData_with_clusters['Bowling Cluster'][j]

    team1BatClust=list(batClustT1.values())
    team2BatClust=list(batClustT2.values())
    team1BowlClust=list(bowlClustT1.values())
    team2BowlClust=list(bowlClustT2.values())
    
    overs = 1
    balls = 1
    runs=0
    wickets = 0
    innings=1
    indexOfBatsmanOnStrike=0
    indexOfNonStriker = 1
    indexOfWicket = 1
    indexOfBowler=-1
    data1 = []
    
#     print("overs","balls","runs","total runs","wickets","total wickets",sep=" |")
    while overs<=20 and wickets<10:
        while balls<=6 and wickets<10:
            r = []
            arr = np.array([[innings,overs,balls,team1BatClust[indexOfBatsmanOnStrike],team2BowlClust[indexOfBowler]]])
            runs_pred = loaded_model_runs.predict(arr)
            runs_pred = runs_pred.astype(int)
            wickets_pred = loaded_model_wickets.predict(arr)
            runs +=runs_pred[0]
            wickets +=wickets_pred[0]
            r.append(overs)
            r.append(balls)
            r.append(runs_pred[0])
            r.append(runs)
            r.append(wickets_pred[0])
            r.append(wickets)
            data1.append(r)
            
#             print(overs,balls,runs_pred[0],runs,wickets_pred[0],wickets,sep="\t|")
            if wickets_pred==1:
                indexOfWicket+=1
                indexOfBatsmanOnStrike = indexOfWicket
            if runs_pred == 1 or runs_pred == 3:
                temp = indexOfBatsmanOnStrike
                indexOfBatsmanOnStrike=indexOfNonStriker
                indexOfNonStriker=temp
            balls+=1
        temp = indexOfBatsmanOnStrike
        indexOfBatsmanOnStrike=indexOfNonStriker
        indexOfNonStriker=temp
        overs+=1
        balls=1
        indexOfBowler-=1
        if indexOfBowler==-6:
            indexOfBowler=-1


    overs = 1
    balls = 1
    runs=0
    wickets = 0
    innings=1
    indexOfBatsmanOnStrike=0
    indexOfNonStriker = 1
    indexOfWicket = 1
    indexOfBowler=-1
    data2 = []
#     print("overs","balls","runs","total runs","wickets","total wickets",sep=" |")
    while overs<=20 and wickets<10:
        while balls<=6 and wickets<10:
            r = []
            arr = np.array([[innings,overs,balls,team2BatClust[indexOfBatsmanOnStrike],team1BowlClust[indexOfBowler]]])
            runs_pred = loaded_model_runs.predict(arr)
            runs_pred = runs_pred.astype(int)
            wickets_pred = loaded_model_wickets.predict(arr)
            runs +=runs_pred[0]
            wickets +=wickets_pred[0]
            r.append(overs)
            r.append(balls)
            r.append(runs_pred[0])
            r.append(runs)
            r.append(wickets_pred[0])
            r.append(wickets)
            data2.append(r)
#             print(overs,balls,runs_pred[0],runs,wickets_pred[0],wickets,sep="\t|")
            if wickets_pred==1:
                indexOfWicket+=1
                indexOfBatsmanOnStrike = indexOfWicket
            if runs_pred == 1 or runs_pred == 3:
                temp = indexOfBatsmanOnStrike
                indexOfBatsmanOnStrike=indexOfNonStriker
                indexOfNonStriker=temp
            balls+=1
        temp = indexOfBatsmanOnStrike
        indexOfBatsmanOnStrike=indexOfNonStriker
        indexOfNonStriker=temp
        overs+=1
        balls=1
        indexOfBowler-=1
        if indexOfBowler==-6:
            indexOfBowler=-1

    df1 = pd.DataFrame(data1, columns =["Overs","Balls","Runs","Total_runs","Wickets","Total_wickets"])
    df2 = pd.DataFrame(data2, columns =["Overs","Balls","Runs","Total_runs","Wickets","Total_wickets"])

    allData1 = []
    for i in range(df1.shape[0]):
        temp = df1.loc[i]
        allData1.append(dict(temp))

    allData2 = []
    for i in range(df2.shape[0]):
        temp = df2.loc[i]
        allData2.append(dict(temp))

    return render(request, "result.html",{'ans1': allData1,'ans2': allData2})
