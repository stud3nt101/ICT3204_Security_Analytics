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
        self.dataset_path = os.path.abspath(os.path.join(self.basepath,".","binetflow"))
        self.directory = os.fsencode(self.dataset_path)
        self.model = xgb.XGBClassifier(use_label_encoder=False, scale_pos_weight = 1.2, max_depth=8)
        self.bst = None
        pass

    def load_model(self, filename) -> XGBClassifier():
        try:
            self.model.load_model(filename)
        except:
            sys.stdout.write (f"Model can't be load, wrong model name")
            sys.stdout.flush()
            exit()
        
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
        a = 0 
        for i in pred:
            if i == 1: count += 1 
            else: a += 1
        verdict = True if count > (len(pred)*0.8) else False   
        print(f"Bad: {count}")
        print (f"Good: {a}")
        print(f"Verdict: {verdict}")
        return verdict
        

    def create_model(self) -> XGBClassifier():
        print('Processing data set...')
        progress = ''
        for count,f in enumerate (os.listdir(self.directory)):
            f_name = os.fsdecode(f)
            if f_name.endswith(".binetflow"):
                p = os.path.join(self.dataset_path, f_name)
                
                LoadData.loaddata(p, label=True)
                file = open(os.path.join(self.basepath,'flowdata.pickle'), 'rb')
                data = pickle.load(file)

                X = data[0]
                y = data[1]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
                

                self.model.fit(X_train, y_train, xgb_model=self.bst)

                y_pred = self.model.predict(X_test)
                predictions = [round(value) for value in y_pred]
                accuracy = accuracy_score(y_test, predictions)
                print("Accuracy: %.2f%%" % (accuracy * 100.0))
                    
                self.model.save_model("xgbmodel"+str(count))
                self.bst = "xgbmodel"+str(count)
                
                # progress bar
                progress = progress + '=' * 6
                sys.stdout.write('%d/13 Files %s\r' % (count+1,progress))
                sys.stdout.flush()

        return self.model

#Usage example
if __name__ == "__main__":
    ML = ML_Prediction()
    # To train a model
    # ML.create_model()
    
    #load a model and make prediction 
    ML.load_model("xgbmodel12")
    ML.prediction("secure-server.binetflow")
    
