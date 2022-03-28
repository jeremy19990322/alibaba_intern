# -*- coding: utf-8 -*-

# -- Sheet --


import pandas as pd
import numpy as np

data = pd.read_csv("ShoppingData.csv")
#data.drop(data[data.stock == "Currently unavailable."].index)
#**把数据中Currently unavailable的数据行删除**
data = data.drop_duplicates()
data = data[data.stock != "Currently unavailable."]
data = data[data.price != 0]
data = data.dropna()
data["rank_big"] = data["rank_big"].replace(0.0, np.nan)
new_data = data.fillna(method = "backfill")
print(new_data.value_counts("class0"))

###连续变量离散处理

#(1) 小类排名：<=10，>10
rank1_max = new_data.rank1_list.max()
#print(rank1_max)
rank1_list_cut = pd.cut(new_data["rank1_list"],[0, 10, 50], right=True, labels=("top10", "other"))
#print(rank1_list_cut)

#(2) reviews评论：按照50,100,300,1000,1500,2000和大于2000

reviews_cut = pd.cut(new_data["reviews"], [-0.1, 50, 100, 300, 1000, 1500, 2000, new_data.reviews.max()], right=True,
                           labels=("reviews#<=50", "reviews#<=100", "reviews#<=300", "reviews#<=1000", "reviews#<=1500", "reviews#<=2000", "reviews#>2000"))
#reviews_cut

#(3) 价格：按照0-180内每隔20划分，大于180是一个,得到10个区间
price_cut = pd.cut(new_data["price"], [0,20, 40, 60, 80, 100, 120, 140, 160, 180, new_data.price.max()], right=True,
                   labels= (" p<20"," 20<p<=40", " 40<p<=60", " 60<p<=80", " 80<p<=100", " 100<p<=120", " 120<p<=140", " 140<=p160", " 160<p<=180", " p>180"))
#print(price_cut)

#(4) stars：0,1,2,3,4,5
stars_cut = pd.cut(new_data["stars"], [-0.1, 1, 2, 3, 4, 5], right = True,
                   labels=("0<=star<1", "1<star<=2", "2<star<=3", "3<star<=4", "4<star<=5"))
#print(stars_cut)

#(5) rank_big:'0-500','500-1000','1000-5000','5000-10000','10000-50000','50000-100000','>100000，得到7个区间
rank_big_cut = pd.cut(new_data["rank_big"], [0, 500, 1000, 5000, 10000, 50000, 100000, new_data.rank_big.max()], right=False,
                      labels=("top500", "top1000", "top5000", "top10000", "top50000", "top100000", "ranking over 100000"))
#print(rank_big_cut)
cut_data = new_data
cut_data["rank1_list"] = rank1_list_cut
cut_data["price"] = price_cut
cut_data["stars"] = stars_cut
cut_data["reviews"] = reviews_cut
cut_data["rank_big"] = rank_big_cut

price_cut_n = cut_data.price.cat.codes
reviews_cut_n = cut_data.reviews.cat.codes
stars_cut_n = cut_data.stars.cat.codes
rank_big_cut_n = cut_data.rank_big.cat.codes

cut_data["price_cut_n"] = price_cut_n
cut_data["reviews_cut_n"] = reviews_cut_n
cut_data["stars_cut_n"] = stars_cut_n
cut_data["rank_big_cut_n"] = rank_big_cut_n

#同向化
#print(cut_data.reviews_cut_n.max())
#pd.DataFrame = cut_data
#cut_data["reviews_cut_n"] - 7
#cut_data["reviews_cut_n"].replace(2, 5)
#cut_data["reviews_cut_n"].replace(3, 4)
#cut_data["reviews_cut_n"].replace(4, 3)
#cut_data["reviews_cut_n"].replace(5, 2)
#cut_data["reviews_cut_n"].replace(6, 1)
cut_data








    











# The ShoppingData is pre-processed by deleting rows conditioned by 0 or null value regarding price and brand; Rank value with 0 is replaced by the data behind. Therefore, ShoppingData is ready for further analyzing, while we do not consider class 6 or 11 since the quantity of their products is less than 40 by counting methods [.value_counts("class0")]


import pandas as pd
import numpy as np
data = pd.read_csv("cutShoppingData.csv")
data.shape, data.info

