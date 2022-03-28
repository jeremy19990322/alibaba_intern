# -*- coding: utf-8 -*-

# -- Sheet --

import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
data = pd.read_csv("goods_list_new.csv",encoding="gb18030")
train = data[data["关键词"] == "咖啡机"]
train  = train[['付款人数', '同类商品浏览次数']]
train.info()
r_train = train.corr()
exam_x = train['同类商品浏览次数']
exam_y = train['付款人数']
exam_x = exam_x.reset_index(drop = True)
exam_y = exam_y.reset_index(drop=True)
x_train, x_test, y_train, y_test = train_test_split(exam_x, exam_y, train_size = 0.8)
print(exam_x.shape, x_train.shape, x_test.shape)
print(exam_y.shape, y_train.shape, y_test.shape)
plt.scatter(x_train, y_train)
plt.xlabel('view_sub')
plt.ylabel('deal_num')

y_train = y_train.reset_index(drop=True)
y_train = y_train.fillna(y_train.mean())
print(np.isinf(y_test).any(),
np.isfinite(y_test).all(),
np.isnan(y_test).any())


x_train = x_train.values.reshape(-1, 1)
x_test = x_test.values.reshape(-1, 1)

model = LinearRegression()
model.fit(x_train, y_train)

intercept = model.intercept_
coef = model.coef_
print("最小二乘直线方程为: y={} + {}x".format(intercept, coef))
#print(model.score(x_test, y_test))
y_train_pred = model.predict(x_train)

plt.figure(figsize=(8,6))
plt.scatter(x_train, y_train, c='b', label = 'training set')
plt.scatter(x_test, y_test, c='r', label = 'testing set')
plt.plot(x_train, y_train_pred, c='g', linewidth=2, label='OLS line')
plt.xlabel("view_sub")
plt.ylabel("number of deals")
plt.legend(loc='upper left')


