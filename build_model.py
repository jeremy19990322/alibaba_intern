# -*- coding: utf-8 -*-

# -- Sheet --



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use(style="ggplot")
import seaborn as sns
sns.set(font="simhei")
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import linear_model

data = pd.read_csv("goods_list_new.csv",encoding="gb18030")


train = data[["付款人数","产品价格", "浏览停留时间(min)","同类商品浏览次数", "评论数", "收藏数"]]
#需要把付款人数数据类型改变
train["付款人数"] = train["付款人数"].fillna('0').astype('int64' , errors='ignore' )

train.columns = ['num_deals','price', 'visiting_time(min)', 'visit_similar_times', 'num_reviews', 'num_marked']


print(train.info())
print(train.num_deals.describe().astype(int))

corrMat = train[['num_deals','price', 'visiting_time(min)', 'visit_similar_times', 'num_reviews', 'num_marked']].corr()
mask = np.array(corrMat)
mask[np.tril_indices_from(mask)] = False
plt.subplots(figsize=(20,10))
plt.xticks(rotation=60)#设置刻度标签角度
sns.heatmap(corrMat, mask=mask,vmax=.8, square=True,annot=True)

features = ['num_deals','price', 'visiting_time(min)', 'visit_similar_times', 'num_reviews', 'num_marked']
X = train[features]
y = np.log(train['num_deals'])
#print(X.shape,y.shape)
train = train.reset_index()

X_copy = X[:]

scaler = MinMaxScaler()
X_transformed = scaler.fit_transform(X_copy)


X_train,X_test,y_train,y_test = train_test_split(X_transformed,y,
                                                 random_state=1,test_size=.2)
y_train = y_train.reset_index(drop=True)
y_train = y_train.dropna()
print(np.isinf(y_train).any(),
np.isfinite(y_train).all(),
np.isnan(y_train).any())
lm = linear_model.LinearRegression()
model = lm.fit(X_train,y_train)
print(model.intercept_,model.coef_)


