from __future__ import division
import LoadData
import pickle
import pandas as pd
import numpy as np
import os, sys
# import datetime as dt
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost.sklearn import XGBClassifier, XGBModel
# from sklearn import metrics
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import KFold
# from sklearn.model_selection import cross_val_score
# from numpy.core.numeric import cross


class ML_Prediction():
    def __init__(self) -> None:
        self.basepath = os.path.dirname(__file__)
        self.dataset_path = os.path.abspath(os.path.join(self.basepath,".","test"))
        self.directory = os.fsencode(self.dataset_path)
        self.model = xgb.XGBClassifier(use_label_encoder=False, scale_pos_weight = 0.007)
        pass

    def load_model(self, filename) -> XGBClassifier():
        try:
            self.model.load_model(filename)
        except:
            sys.stdout.write (f"Model can't be load, wrong model name")
        
        return self.model
    
    def prediction(self, filename) -> list:
        t_path = os.path.abspath(os.path.join(self.basepath,".","import"))
        p = os.path.join(t_path, filename)
        LoadData.loaddata(p)
        file = open(os.path.join(self.basepath,'flowdata.pickle'), 'rb')
        data = pickle.load(file)
        X = data[0]
        print(len(X))
        pred = self.model.predict(X)
        count = 0 
        for i in pred:
            if i == 1: count += 1 
        verdict = True if count > (len(pred)*0.5) else False   
        print(count)
        print(verdict)
        return verdict
        

    def create_model(self) -> XGBClassifier():
        print('Processing data set...')
        progress = ''
        for count,f in enumerate (os.listdir(self.directory)):
            f_name = os.fsdecode(f)
            if f_name.endswith(".binetflow"):
            # i = i + 1
            # in here we should us pandas to read the files and do some processing on them
            # just check really fast how we can read the Labels
                p = os.path.join(self.dataset_path, f_name)
                
                LoadData.loaddata(p, label=True)
                file = open(os.path.join(self.basepath,'flowdata.pickle'), 'rb')
                data = pickle.load(file)

                X = data[0]
                y = data[1]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=123)
                

                self.model.fit(X_train, y_train)

                y_pred = self.model.predict(X_test)
                predictions = [round(value) for value in y_pred]
                accuracy = accuracy_score(y_test, predictions)
                print("Accuracy: %.2f%%" % (accuracy * 100.0))
                
                self.model.save_model("xgbmodel")

                print(self.model)        
                
                # progress bar
                progress = progress + '=' * 6
                sys.stdout.write('%d/13 Files %s\r' % (count+1,progress))
                sys.stdout.flush()

        return self.model

if __name__ == "__main__":
    ML = ML_Prediction()
    # ML.create_model()
    ML.load_model("xgbmodel")
    ML.prediction("secure-server.binetflow")
    

# basepath = os.path.dirname(__file__)
# dataset_path = os.path.abspath(os.path.join(basepath,".","binetflow"))
# i = 0
# print('Processing data set...')
# progress = ''
# directory = os.fsencode(dataset_path)

# model = xgb.XGBClassifier(use_label_encoder=False)
# model.load_model("xgbmodel")

# t_path = os.path.abspath(os.path.join(basepath,".","binetflow"))
# p = os.path.join(t_path, "capture20110819.binetflow")
# LoadData.loaddata(p)
# file = open(os.path.join(basepath,'flowdata.pickle'), 'rb')
# data = pickle.load(file)

# X = data[0]
# y = data[1]
# print(X)
# pred = model.predict(X)
# print(pred)
# count = 0
# for i in pred:
#     if i == 1:
#         count+=1
# print(count)
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