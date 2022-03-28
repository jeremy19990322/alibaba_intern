# -*- coding: utf-8 -*-

# -- Sheet --

import pandas as pd
import numpy as np


data = pd.read_csv("task1_ShoppingData_fixed.csv")
ori_data = pd.read_csv("task1_ShoppingData_fixed.csv")
data = data.drop(["drop", "num_top_brand"], axis = 1)
ori_data = ori_data.drop(["drop", "num_top_brand"], axis = 1)



#normalization
for i in data.columns[1:]:
    Max = np.max(data[i])
    Min = np.min(data[i]) 
    data[i] = (data[i] - Min)/(Max - Min)

# calculate prob
for i in data.columns[1:]:
    data[i] = data[i]/sum(data[i]) + 0.00001

#calculate Entropy
E = pd.DataFrame(columns=data.columns[1:],index=["Entropy"])
for j in E.columns:
    s = sum(data[j] * np.log(data[j]))
    E[j] = (-1/np.log(len(data))) * s

#calculate Weight
W = pd.DataFrame(columns=data.columns[1:], index = ["Weight"])
for i in W.columns:
    W[i] = (1 - E[i].values) / (12 -sum(E[i].values))

#calculate score


list_1 = []
for i in range(len(data)):
    list_1.append(np.sum(ori_data.iloc[i, 1:]* W).sum())


ori_data["score"] = list_1
score = pd.concat([W,E, ori_data])
score.to_csv("Score.csv")



 










