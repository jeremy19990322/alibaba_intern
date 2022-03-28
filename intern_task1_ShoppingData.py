# -*- coding: utf-8 -*-

# -- Sheet --

import pandas as pd
import numpy as np

data = pd.read_csv("ShoppingData.csv")
data = data.drop_duplicates()
data = data[data.stock != "Currently unavailable."]
data = data[data.price != 0]
data = data.dropna()
data["rank_big"] = data["rank_big"].replace(0.0, np.nan)
new_data = data.fillna(method = "backfill")

#review_top50 = new_data.sort_values(by = ["reviews"], ascending = False).head(50)
reviews_cut = pd.cut(new_data["reviews"], [-0.1, 50, 100, 300, 1000, 1500, 2000, new_data.reviews.max()], right=True,
                           labels=("reviews#<=50", "reviews#<=100", "reviews#<=300", "reviews#<=1000", "reviews#<=1500", "reviews#<=2000", "reviews#>2000"))
new_data["reviews_cut_n"] = (reviews_cut.cat.codes - (reviews_cut.cat.codes.max() + 1)) * (-1) 
new_data.value_counts("reviews_cut_n")

# 确定并实现指标体系：通过新建表格df_final，数据项为
# 
# Class0,大类类别
# 
# reviews-median_top_50，review量top50的中位数
# reviews_cut_n_most_top_10，review量top10的区间最多的是多少
# 
# brand_count，品牌数量
# brand_top_ratio，数量最多的品牌产品数量占比
# 
# rank_big_cut_n_most_top_10，top10的产品大类排名的区间
# rank_big_80_top_50，top50的产品大类排名80%的排名在多少
# 
# stars_cut_n_most_top_10，top10 stars的区间最多的是多少
# stars-mean_top_50，top50 stars的平均数是多少
# 
# r_p，
# 
# price-median_top_50，top50 price的中位数是多少
# price_cut_n_most_top_10，top10 price的区间最多的是多少
# price_80_top_10，top10 price的价格80%是多少
#  
# 整理并输出一张excel表格


