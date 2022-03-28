# -*- coding: utf-8 -*-

# -- Sheet --

import datetime
import pandas as pd
import numpy as np

final_table = pd.read_excel("final_table_5.31.xlsx")
final_table.to_csv("final_table_5.31.csv")
final_table = pd.read_csv("final_table_5.31.csv")
sales_ad = pd.read_csv("sales_ad.csv")
sales_all = pd.read_csv("sales_all.csv")
sales_detail = pd.read_csv("sales_detail.csv")
sales_stock = pd.read_csv("sales_stock.csv")
sales_url = pd.read_csv("sales_url.csv")


###页面信息
sales_url_5_31 = sales_url[sales_url["insert_date"] == "2021/5/31"]
rank_big = []
rank_small = []
reviews = []
price = []
star = []
for product_id in final_table["商品ID"]:
    rank_big.append(sales_url_5_31[sales_url_5_31["product_ID"] == product_id]["sales_rank"].values[0])
    rank_small.append(sales_url_5_31[sales_url_5_31["product_ID"] == product_id]["rank_small"].values[0])
    reviews.append(sales_url_5_31[sales_url_5_31["product_ID"] == product_id]["reviews"].values[0])
    price.append(sales_url_5_31[sales_url_5_31["product_ID"] == product_id]["price"].values[0])
    star.append(sales_url_5_31[sales_url_5_31["product_ID"] == product_id]["stars"].values[0])

final_table["大类排名"] = rank_big
final_table["小类排名"] = rank_small
final_table["评论数"] = reviews
final_table["价格"] = price
final_table["星级"] = star

###广告相关
sales_ad_5_31 = sales_ad[sales_ad["end_day"] == "2021/5/31"]
#曝光量
exposure_times = []
#点击数
clicks = []
#广告花费
cost = []
#广告带来销量
sales_ad_list = []
#广告带来销售额
gmv_ad = []

for product_id in final_table["商品ID"]:
    try:
        exposure_times.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["exposure_times"].values[0])
    except IndexError:
        exposure_times.append(0)
for product_id in final_table["商品ID"]:
    try:
        clicks.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["clicks"].values[0])
    except IndexError:
        clicks.append(0)
for product_id in final_table["商品ID"]:
    try:
        cost.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["cost"].values[0])
    except IndexError:
        cost.append(0)
for product_id in final_table["商品ID"]:
    try:
        sales_ad_list.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["sales_ad"].values[0])
    except IndexError:
        sales_ad_list.append(0)
for product_id in final_table["商品ID"]:
    try:
        gmv_ad.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["gmv_ad"].values[0])
    except IndexError:
        gmv_ad.append(0)
        #gmv_ad.append(sales_ad_5_31[sales_ad_5_31["product_ID"] == product_id]["gmv_ad"])


final_table["曝光量"] = exposure_times
final_table["点击数"] = clicks
final_table["广告花费"] = cost
final_table["广告带来销量"] = sales_ad_list
final_table["广告带来销售额"] = gmv_ad

#点击率 = 点击数/曝光量
final_table["点击率CTR"] = final_table["点击数"]/final_table["曝光量"]

#CPC = click / cost
final_table["按点击收费CPC"] = final_table["点击数"]/final_table["广告花费"]
#ACoS = 广告投入/销售额
final_table["ACoS"] = final_table["广告花费"]/final_table["广告带来销售额"]


###销售信息
sales_detail_5_31 = sales_detail[sales_detail["update_day"] == "2021/5/31"]
orders_count_5_31=[]


orders_count = []
gmv = []
for product_id in final_table["商品ID"]:
    try:
        orders_count.append(sales_detail_5_31[sales_detail_5_31["product_ID"] == product_id]["orders_count"].values[0])
    except IndexError:
        exposure_times.append(0)
for product_id in final_table["商品ID"]:
    try:
        gmv.append(sales_detail_5_31[sales_detail_5_31["product_ID"] == product_id]["gmv"].values[0])
    except IndexError:
        exposure_times.append(0)


final_table["销量"] = orders_count
final_table["销售额"] = gmv
#final_table["近7日销量"] = orders_count_7days

#库存物流相关
sales_per_day = []
curr_stock = []
sold_out_est = []



sales_stock_5_31 = sales_stock[sales_stock["update_day"] == "2021/5/31"]

for product_id in final_table["商品ID"]:
    try:
        curr_stock.append(sales_stock_5_31[sales_stock_5_31["product_ID"] == product_id]["in_stock"].values[0])
    except IndexError:
        exposure_times.append(0)


for product_id in final_table["商品ID"]:
    try:
        sales_per_day.append(sales_detail[sales_detail["product_ID"] == product_id]["orders_count"].values.mean())
    except IndexError:
        exposure_times.append(0)

final_table["日均销量预估"] = sales_per_day
final_table["当前库存"] = curr_stock
final_table["售完预计天数"] = final_table["当前库存"]/final_table["日均销量预估"]
final_table["date"] = pd.to_datetime(final_table["日期"], format='%Y.%m.%d')
sales_detail["date"] = pd.to_datetime(sales_detail["update_day"], format='%Y.%m.%d')
#sales_detail[(sales_detail["date"] > datetime.datetime(2021,5,25))&(sales_detail["date"] < datetime.datetime(2021,5,31))]

orders_count_7days = []
sales_detail_7day = sales_detail[(sales_detail["date"] > datetime.datetime(2021,5,25))&(sales_detail["date"] < datetime.datetime(2021,5,31))]
for product_id in final_table["商品ID"]:
    try:
        orders_count_7days.append(sum(sales_detail_7day[sales_detail_7day["product_ID"] == product_id]["orders_count"].values))
    except IndexError:
        exposure_times.append(0)

final_table["近7日销量"] = orders_count_7days
final_table["近7日平均销量"] = final_table["近7日销量"]/7






#a = sales_detail[sales_detail["product_ID"] == "B07S4HN2XX"].index
#a

sale_detail_drop = sales_detail["orders_count"].replace(0, np.NaN)
sales_detail["orders_count"] = sale_detail_drop
sales_detail=sales_detail.dropna()
sales_detail_new = sales_detail[sales_detail["date"] != datetime.datetime(2021,5,31)]

date_count = []
for product_id in final_table["商品ID"]:
    ID = sales_detail_new[sales_detail_new["product_ID"] == product_id]
    date_count.append(datetime.datetime(2021,5,31) - (ID.iloc[-1]["date"]))

final_table["最晚售出距今天数"] = date_count
final_table = final_table.replace(np.inf, np.NaN)
final_table.replace(np.NaN, 0)
final_table.to_excel("final_table_2.0.xlsx")



