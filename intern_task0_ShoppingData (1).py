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
#new_data.value_counts("class0")

###连续变量离散处理

#(1) 小类排名：<=10，>10
rank1_max = new_data.rank1_list.max()
#print(rank1_max)
new_data["rank1_list_cut"] = pd.cut(new_data["rank1_list"],[0, 10, 50], right=True, labels=("top10", "other"))
#print(rank1_list_cut)

#(2) reviews评论：按照50,100,300,1000,1500,2000和大于2000

new_data["reviews_cut"] = pd.cut(new_data["reviews"], [-0.1, 50, 100, 300, 1000, 1500, 2000, new_data.reviews.max()], right=True,
                           labels=("reviews#<=50", "reviews#<=100", "reviews#<=300", "reviews#<=1000", "reviews#<=1500", "reviews#<=2000", "reviews#>2000"))
#reviews_cut

#(3) 价格：按照0-180内每隔20划分，大于180是一个,得到10个区间
new_data["price_cut"] = pd.cut(new_data["price"], [0,20, 40, 60, 80, 100, 120, 140, 160, 180, new_data.price.max()], right=True,
                   labels= (" p<20"," 20<p<=40", " 40<p<=60", " 60<p<=80", " 80<p<=100", " 100<p<=120", " 120<p<=140", " 140<=p160", " 160<p<=180", " p>180"))
#print(price_cut)

#(4) stars：0,1,2,3,4,5
new_data["stars_cut"] = pd.cut(new_data["stars"], [-0.1, 1, 2, 3, 4, 5], right = True,
                   labels=("0<=star<1", "1<star<=2", "2<star<=3", "3<star<=4", "4<star<=5"))
#print(stars_cut)

#(5) rank_big:'0-500','500-1000','1000-5000','5000-10000','10000-50000','50000-100000','>100000，得到7个区间
new_data["rank_big_cut"] = pd.cut(new_data["rank_big"], [0, 500, 1000, 5000, 10000, 50000, 100000, new_data.rank_big.max()], right=False,
                      labels=("top500", "top1000", "top5000", "top10000", "top50000", "top100000", "ranking over 100000"))
#print(rank_big_cut)
cut_data = new_data
#cut_data["rank1_list"] = rank1_list_cut
#cut_data["price"] = price_cut
#cut_data["stars"] = stars_cut
#cut_data["reviews"] = reviews_cut
#cut_data["rank_big"] = rank_big_cut


price_cut_n = new_data.price_cut.cat.codes + 1
reviews_cut_n = (new_data.reviews_cut.cat.codes - (cut_data.reviews_cut.cat.codes.max() + 1)) * (-1) 
stars_cut_n = new_data.stars_cut.cat.codes + 1
rank_big_cut_n = (new_data.rank_big_cut.cat.codes - (cut_data.rank_big_cut.cat.codes.max() + 1)) * (-1)

new_data["price_cut_n"] = price_cut_n
new_data["reviews_cut_n"] = reviews_cut_n
new_data["stars_cut_n"] = stars_cut_n
new_data["rank_big_cut_n"] = rank_big_cut_n
new_data["r_p"] = reviews_cut_n * price_cut_n
#new_data.to_csv("task0_ShoppingData_fixed.csv")


#df_final = new_data
#top50 = df_final.sort_values(by = ["rank_big"], ascending = True).head(50)
#top10 = df_final.sort_values(by = ["rank_big"], ascending = True).head(10)
#df_final["reviews-median_top_50"] = top50["reviews"].median()
#df_final["reviews_cut_n_most_top_10"] = top10["reviews_cut_n"].value_counts()
#new_data["brand"].value_counts()
#brand_top_ratio = 22/235
#top50["stars"].mean()
#top50["price"].median()
#df_final["price_cut_n_most_top_10"] = top10["price_cut_n"].value_counts()
#print(top10["price_cut_n"].value_counts())

df_final = pd.DataFrame(columns=["Class0", "reviews-median_top_50", "reviews_cut_n_most_top_10", "brand_count", 
                                 "brand_top_ratio", "rank_big_cut_n_most_top_10", "rank_big_80_top_50", "stars_cut_n_most_top_10", 
                                 "stars-mean_top_50", "r_p", "price-median_top_50", "price_cut_n_most_top_10", 
                                 "price_80_top_10"], index=[1,2,3,4,5,6,7,8,9,10,11])
df_final["Class0"] = ["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11"]
x1_top50 = new_data[new_data.class0 == "x1"].sort_values(by = "rank1_list", ascending = True).head(50)
x2_top50 = new_data[new_data.class0 == "x2"].sort_values(by = "rank1_list", ascending = True).head(50)
x3_top50 = new_data[new_data.class0 == "x3"].sort_values(by = "rank1_list", ascending = True).head(50)
x4_top50 = new_data[new_data.class0 == "x4"].sort_values(by = "rank1_list", ascending = True).head(50)
x5_top50 = new_data[new_data.class0 == "x5"].sort_values(by = "rank1_list", ascending = True).head(50)
x6_top50 = new_data[new_data.class0 == "x6"].sort_values(by = "rank1_list", ascending = True).head(50)
x7_top50 = new_data[new_data.class0 == "x7"].sort_values(by = "rank1_list", ascending = True).head(50)
x8_top50 = new_data[new_data.class0 == "x8"].sort_values(by = "rank1_list", ascending = True).head(50)
x9_top50 = new_data[new_data.class0 == "x9"].sort_values(by = "rank1_list", ascending = True).head(50)
x10_top50 = new_data[new_data.class0 == "x10"].sort_values(by = "rank1_list", ascending = True).head(50)
x11_top50 = new_data[new_data.class0 == "x11"].sort_values(by = "rank1_list", ascending = True).head(50)

x1_top10 = new_data[new_data.class0 == "x1"].sort_values(by = "rank1_list", ascending = True).head(10)
x2_top10 = new_data[new_data.class0 == "x2"].sort_values(by = "rank1_list", ascending = True).head(10)
x3_top10 = new_data[new_data.class0 == "x3"].sort_values(by = "rank1_list", ascending = True).head(10)
x4_top10 = new_data[new_data.class0 == "x4"].sort_values(by = "rank1_list", ascending = True).head(10)
x5_top10 = new_data[new_data.class0 == "x5"].sort_values(by = "rank1_list", ascending = True).head(10)
x6_top10 = new_data[new_data.class0 == "x6"].sort_values(by = "rank1_list", ascending = True).head(10)
x7_top10 = new_data[new_data.class0 == "x7"].sort_values(by = "rank1_list", ascending = True).head(10)
x8_top10 = new_data[new_data.class0 == "x8"].sort_values(by = "rank1_list", ascending = True).head(10)
x9_top10 = new_data[new_data.class0 == "x9"].sort_values(by = "rank1_list", ascending = True).head(10)
x10_top10 = new_data[new_data.class0 == "x10"].sort_values(by = "rank1_list", ascending = True).head(10)
x11_top10 = new_data[new_data.class0 == "x11"].sort_values(by = "rank1_list", ascending = True).head(10)

###reviews
df_final["reviews-median_top_50"] = [x1_top50["reviews"].median(),
                                  x2_top50["reviews"].median(),
                                  x3_top50["reviews"].median(),
                                  x4_top50["reviews"].median(),
                                  x5_top50["reviews"].median(),
                                  x6_top50["reviews"].median(),
                                  x7_top50["reviews"].median(),
                                  x8_top50["reviews"].median(),
                                  x9_top50["reviews"].median(),
                                  x10_top50["reviews"].median(),
                                  x11_top50["reviews"].median()]


df_final["reviews_cut_n_most_top_10"] = [x1_top10["reviews_cut_n"].mode().values[0],
                                         x2_top10["reviews_cut_n"].mode().values[0],
                                         x3_top10["reviews_cut_n"].mode().values[0],
                                         x4_top10["reviews_cut_n"].mode().values[0],
                                         x5_top10["reviews_cut_n"].mode().values[0],
                                         x6_top10["reviews_cut_n"].mode().values[0],
                                         x7_top10["reviews_cut_n"].mode().values[0],
                                         x8_top10["reviews_cut_n"].mode().values[0],
                                         x9_top10["reviews_cut_n"].mode().values[0],
                                         x10_top10["reviews_cut_n"].mode().values[0],
                                         x11_top10["reviews_cut_n"].mode().values[0]]

#x1_top10["reviews_cut_n"].value_counts()

###brand

df_final["brand_count"] = [new_data[new_data.class0 == "x1"]["brand"].nunique(),
                           new_data[new_data.class0 == "x2"]["brand"].nunique(),
                           new_data[new_data.class0 == "x3"]["brand"].nunique(),
                           new_data[new_data.class0 == "x4"]["brand"].nunique(),
                           new_data[new_data.class0 == "x5"]["brand"].nunique(),
                           new_data[new_data.class0 == "x6"]["brand"].nunique(),
                           new_data[new_data.class0 == "x7"]["brand"].nunique(),
                           new_data[new_data.class0 == "x8"]["brand"].nunique(),
                           new_data[new_data.class0 == "x9"]["brand"].nunique(),
                           new_data[new_data.class0 == "x10"]["brand"].nunique(),
                           new_data[new_data.class0 == "x11"]["brand"].nunique()]

df_final["num_top_brand"] = [new_data[new_data.class0 == "x1"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x2"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x3"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x4"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x5"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x6"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x7"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x8"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x9"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x10"]["brand"].value_counts().max(),
                        new_data[new_data.class0 == "x11"]["brand"].value_counts().max()]
df_final["brand_top_ratio"] = df_final.num_top_brand / df_final.brand_count


# rank_big

df_final["rank_big_cut_n_most_top_10"] = [x1_top10["rank_big_cut_n"].mode().values[0],
                                          x2_top10["rank_big_cut_n"].mode().values[0],
                                          x3_top10["rank_big_cut_n"].mode().values[0],
                                          x4_top10["rank_big_cut_n"].mode().values[0],
                                          x5_top10["rank_big_cut_n"].mode().values[0],
                                          x6_top10["rank_big_cut_n"].mode().values[0],
                                          x7_top10["rank_big_cut_n"].mode().values[0],
                                          x8_top10["rank_big_cut_n"].mode().values[0],
                                          x9_top10["rank_big_cut_n"].mode().values[0],
                                          x10_top10["rank_big_cut_n"].mode().values[0],
                                          x11_top10["rank_big_cut_n"].mode().values[0]]
df_final
#df_final["rank_big_80_top_50"] 




#star

df_final["stars_cut_n_most_top_10"] =  [x1_top10["stars_cut_n"].mode().values[0],
                                        x2_top10["stars_cut_n"].mode().values[0],
                                        x3_top10["stars_cut_n"].mode().values[0],
                                        x4_top10["stars_cut_n"].mode().values[0],
                                        x5_top10["stars_cut_n"].mode().values[0],
                                        x6_top10["stars_cut_n"].mode().values[0],
                                        x7_top10["stars_cut_n"].mode().values[0],
                                        x8_top10["stars_cut_n"].mode().values[0],
                                        x9_top10["stars_cut_n"].mode().values[0],
                                        x10_top10["stars_cut_n"].mode().values[0],
                                        x11_top10["stars_cut_n"].mode().values[0]]
df_final["stars-mean_top_50"] = [x1_top50["stars"].mean(),
                                 x2_top50["stars"].mean(),
                                 x3_top50["stars"].mean(),
                                 x4_top50["stars"].mean(),
                                 x5_top50["stars"].mean(),
                                 x6_top50["stars"].mean(),
                                 x7_top50["stars"].mean(),
                                 x8_top50["stars"].mean(),
                                 x9_top50["stars"].mean(),
                                 x10_top50["stars"].mean(),
                                 x11_top50["stars"].mean()]
df_final["r_p"] = [new_data[new_data.class0 == "x1"]["r_p"].mean(),
                   new_data[new_data.class0 == "x2"]["r_p"].mean(),
                   new_data[new_data.class0 == "x3"]["r_p"].mean(),
                   new_data[new_data.class0 == "x4"]["r_p"].mean(),
                   new_data[new_data.class0 == "x5"]["r_p"].mean(),
                   new_data[new_data.class0 == "x6"]["r_p"].mean(),
                   new_data[new_data.class0 == "x7"]["r_p"].mean(),
                   new_data[new_data.class0 == "x8"]["r_p"].mean(),
                   new_data[new_data.class0 == "x9"]["r_p"].mean(),
                   new_data[new_data.class0 == "x10"]["r_p"].mean(),
                   new_data[new_data.class0 == "x11"]["r_p"].mean()]
# price
df_final["price-median_top_50"] = [x1_top50["price"].median(),
                                   x2_top50["price"].median(),
                                   x3_top50["price"].median(),
                                   x4_top50["price"].median(),
                                   x5_top50["price"].median(),
                                   x6_top50["price"].median(),
                                   x7_top50["price"].median(),
                                   x8_top50["price"].median(),
                                   x9_top50["price"].median(),
                                   x10_top50["price"].median(),
                                   x11_top50["price"].median()]

df_final["price_cut_n_most_top_10"] = [x1_top10["price_cut_n"].mode().values[0],
                                       x2_top10["price_cut_n"].mode().values[0],
                                       x3_top10["price_cut_n"].mode().values[0],
                                       x4_top10["price_cut_n"].mode().values[0],
                                       x5_top10["price_cut_n"].mode().values[0],
                                       x6_top10["price_cut_n"].mode().values[0],
                                       x7_top10["price_cut_n"].mode().values[0],
                                       x8_top10["price_cut_n"].mode().values[0],
                                       x9_top10["price_cut_n"].mode().values[0],
                                       x10_top10["price_cut_n"].mode().values[0],
                                       x11_top10["price_cut_n"].mode().values[0]]

df_final["price_80_top_10"] =  [x1_top10["price"].quantile(q=0.8),
                                x2_top10["price"].quantile(q=0.8),
                                x3_top10["price"].quantile(q=0.8),
                                x4_top10["price"].quantile(q=0.8),
                                x5_top10["price"].quantile(q=0.8),
                                x6_top10["price"].quantile(q=0.8),
                                x7_top10["price"].quantile(q=0.8),
                                x8_top10["price"].quantile(q=0.8),
                                x9_top10["price"].quantile(q=0.8),
                                x10_top10["price"].quantile(q=0.8),
                                x11_top10["price"].quantile(q=0.8)]

df_final["rank_big_80_top_50"] = [x1_top50["rank_big"].quantile(q=0.8),
                                  x2_top50["rank_big"].quantile(q=0.8),
                                  x3_top50["rank_big"].quantile(q=0.8),
                                  x4_top50["rank_big"].quantile(q=0.8),
                                  x5_top50["rank_big"].quantile(q=0.8),
                                  x6_top50["rank_big"].quantile(q=0.8),
                                  x7_top50["rank_big"].quantile(q=0.8),
                                  x8_top50["rank_big"].quantile(q=0.8),
                                  x9_top50["rank_big"].quantile(q=0.8),
                                  x10_top50["rank_big"].quantile(q=0.8),
                                  x11_top50["rank_big"].quantile(q=0.8)]
df_final.set_index("Class0")
df_final.to_csv("task1_ShoppingData_fixed.csv")


