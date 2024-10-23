import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler


class UserPredictor:
    def fit(self, trainusers, trainlogs, trainclicked):
        model = Pipeline([
        ("pf", PolynomialFeatures(degree = 5, include_bias = False)),
        ("std", StandardScaler()),
        ("lr", LogisticRegression(fit_intercept = False, max_iter = 500)),
        ])
        self.analyze(trainusers, trainlogs, trainclicked)
        trainusers["feature"] = self.logs.values()
        xcols = trainusers[["past_purchase_amt", "age", "feature"]]
        ycol = trainclicked["clicked"]
        self.model = model.fit(xcols, ycol)
        return model.score(xcols, ycol)
    
    def predict(self, testusers, testlogs):
        
        dicty = {}
        for idnum in testusers["id"]:
            dicty[idnum] = 0
        logs = testlogs.set_axis(testlogs["id"])
        for idnum in logs["id"]:
            dicty[idnum] += logs.at[idnum, "duration"].sum()
        self.testlogs = dicty
        testusers["feature"] = self.testlogs.values()
        
        return self.model.predict(testusers[["past_purchase_amt", "age", "feature"]])
    
    def analyze(self, trainusers, trainlogs, trainclicked):
        dicty = {}
        for idnum in trainclicked["id"]:
            dicty[idnum] = 0
        logs = trainlogs.set_axis(trainlogs["id"])
        for idnum in logs["id"]:
            dicty[idnum] += logs.at[idnum, "duration"].sum()
        self.logs = dicty