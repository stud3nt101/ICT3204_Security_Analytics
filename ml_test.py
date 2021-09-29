from __future__ import division
from numpy.core.numeric import cross
import pandas as pd
import numpy as np
import os, sys
import datetime as dt
from sklearn import metrics

from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from xgboost.sklearn import XGBClassifier, XGBModel
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

import LoadData
import pickle


basepath = os.path.dirname(__file__)
dataset_path = os.path.abspath(os.path.join(basepath,".","binetflow"))
i = 0
print('Processing data set...')
progress = ''
directory = os.fsencode(dataset_path)

model = xgb.XGBClassifier(use_label_encoder=False)
model.load_model("xgbmodel")

t_path = os.path.abspath(os.path.join(basepath,".","binetflow"))
p = os.path.join(t_path, "capture20110819.binetflow")
LoadData.loaddata(p)
file = open(os.path.join(basepath,'flowdata.pickle'), 'rb')
data = pickle.load(file)

X = data[0]
y = data[1]
print(X)
pred = model.predict(X)
print(pred)
count = 0
for i in pred:
    if i == 1:
        count+=1
print(count)
#train
# for f in os.listdir(directory):
#     f_name = os.fsdecode(f)
#     if f_name.endswith(".binetflow"):
#         i = i + 1
#         # in here we should us pandas to read the files and do some processing on them
#         # just check really fast how we can read the Labels
#         p = os.path.join(dataset_path, f_name)
#         scene = pd.read_csv(p)
        
#         LoadData.loaddata(p, cross_validation=True)
#         file = open(os.path.join(basepath,'flowdata.pickle'), 'rb')
#         data = pickle.load(file)

#         X = data[0]
#         y = data[1]

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
        

#         model.fit(X_train, y_train)

#         y_pred = model.predict(X_test)
#         predictions = [round(value) for value in y_pred]
#         accuracy = accuracy_score(y_test, predictions)
#         print("Accuracy: %.2f%%" % (accuracy * 100.0))
        
#         model.save_model("xgbmodel")

#         print(model)        
        
#         # progress bar
#         progress = progress + '=' * 6
#         sys.stdout.write('%d/13 Files %s\r' % (i,progress))
#         sys.stdout.flush()

#normal


# import_samples
# cv = True







# if cv == False:
#     X_train = data[0]
#     Y_train =  data[1]
#     X_test = data[2]
#     Y_test = data[3]
# else:
#     X = data[0]
#     Y = data[1]
#     model = xgb.XGBClassifier()
#     kfold = KFold(n_splits=5, shuffle=True, random_state=7)
#     results = cross_val_score(model, X, Y, cv=kfold)
#     print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
#     exit()



# print("X_train: ", X_train)
# print("Y_train: ", Y_train)
# print("X_test: ", X_test)
# print("Y_test: ", Y_test)



# model = XGBClassifier()
# model.fit(X_train, Y_train)
# print(model)

# y_pred = model.predict(X_test)
# predictions = [round(value) for value in y_pred]

# from sklearn.metrics import accuracy_score

# # evaluate predictions
# accuracy = accuracy_score(Y_test, predictions)
# print("Accuracy: %.2f%%" % (accuracy * 100.0))
# print(predictions)