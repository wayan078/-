import os
import numpy as np
import pandas as pd

home_folder =os.path.expanduser("C:\Users\CJCUCSIE\PycharmProjects\untitled2")
data_folder =os.path.join(home_folder,"Data","baseketball")
data_filename =os.path.join(data_folder,"leagues_NBA_2014_games.csv")

result =pd.read_csv(data_filename)
dataset=pd.read_csv(data_filename,parse_dates=["Date"])

dataset.columns=["Date","Start (ET)","Visitor Team","VisitorPts","Home Team","HomePts","OT?","Score Type","Attend","Notes"]

dataset["HomeWin"]=dataset["VisitorPts"] <dataset["HomePts"]
y_true=dataset["HomeWin"].values
dataset["HomeWin"].mean()

print (dataset["HomeWin"].mean())

print ("Home Win percentage:{0:.1f}%".format(100 * dataset["HomeWin"].sum()/dataset["HomeWin"].count()))
#print (dataset.dtypes)

dataset["HomeLastWin"]=False
dataset["VisitorLastWin"]=False
dataset.head()

from collections import defaultdict
won_last=defaultdict(int)

for index,row in dataset.iterrows():
    Home_team=row["Home Team"]
    Visitor_team=row["Visitor Team"]
    row["HomeLastWin"]=won_last[Home_team]
    dataset.set_value(index,"HomeLastWin",won_last[Home_team])
    dataset.set_value(index,"VisitorLastWin",won_last[Visitor_team])
    won_last[Home_team]=int(row["HomeWin"])
    won_last[Visitor_team] = 1 - int(row["HomeWin"])

print (dataset.head(6))

from sklearn.tree import DecisionTreeClassifier
clf=DecisionTreeClassifier(random_state=14)

from sklearn.cross_validation import cross_val_score
X_previoswins=dataset[["HomeLastWin","VisitorLastWin"]].values
clf=DecisionTreeClassifier(random_state=14)
scores=cross_val_score(clf,X_previoswins,y_true,scoring='accuracy')
print ("Using just the last result form the home and visitor teams")
print ("Accuracy:{0:.1f}%".format(np.mean(scores)*100))
