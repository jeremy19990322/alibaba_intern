# -*- coding: utf-8 -*-

# -- Sheet --

import matplotlib.pyplot as plt
import wordcloud
import jieba
import pandas as pd
import re
import numpy as np
import nltk
from nltk.corpus import stopwords
import collections

#数据清洗


def parse(review_content):
    _list = list(review_content)
    n = len(_list)
    if n <= 1:
        print(review_content)
        return
    list1 = []
    for i in range(n - 1):
        if _list[i] != _list[i + 1]:
            list1.append(_list[i])
    list1.append(_list[-1])
    str2 = ''.join(list1)
    return str2


def clean(reviews_data):
    #去重
    reviews_data["content"] = reviews_data["content"].drop_duplicates()
    reviews_data = reviews_data.dropna()
    content_wo_pun = []
    #去除不规范词

    for content in list(reviews_data["content"]):
        #去空格
        content.strip()
        #去标点符号
        punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥～
／·"""
        dicts={i:'' for i in punctuation}
        punc_table=str.maketrans(dicts)
        content_wo_pun.append(re.sub(r"[a-z0-9]","",content.translate(punc_table)))
    
    reviews_data["content"] = content_wo_pun

    content_parsed = []
    for content in list(reviews_data["content"]):
        content_parsed.append(parse(content))
    reviews_data["content"] = content_parsed
    reviews_data = reviews_data.dropna()
    reviews_data.to_csv("curr_review_data_cleaned.csv")


    
#绘制词云
def word_cloud(reviews_data):
    clean(reviews_data)
    with open('curr_review_data_cleaned.csv') as f:
        data = f.read()

# 文本预处理  去除一些无用的字符   只提取出中文出来
    new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
    new_data = " ".join(new_data)

# 文本分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    result_list = []

    with open('中文stopwords.txt', encoding='utf-8') as f:
        con = f.readlines()
        stop_words = set()
    for i in con:
        i = i.replace("\n", "")   # 去掉读取每一行数据的\n
        stop_words.add(i)

    for word in seg_list_exact:
    # 设置停用词并去除单个词
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    print(result_list)
    df = pd.DataFrame()
    #print(df)
    


# 筛选后统计
    word_counts = collections.Counter(result_list)
# 获取前100最高频的词
    word_counts_top100 = word_counts.most_common(100)
    df["w"] = word_counts_top100
    print(df)
    df.to_csv("word_counts.csv",encoding='utf-8')
    print(word_counts_top100)

# 绘制词云
    wc = wordcloud.WordCloud(
        background_color='black',  # 设置背景颜色  默认是black
        width=900, height=600,
        max_words=100,            # 词云显示的最大词语数量
        font_path='SimHei.ttf',   # 设置字体  显示中文
        max_font_size=110,         # 设置字体最大值
        min_font_size=10,         # 设置子图最小值
        random_state=10)           # 设置随机生成状态，即多少种配色方案)
    my_cloud = wc.generate_from_frequencies(word_counts)

# 显示生成的词云图片
    plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
    plt.axis('off')
    plt.show()
    my_cloud.to_file("wordcloud.png")


reviews_data = pd.read_csv("comment_con 巴拉巴拉.csv")
word_cloud(reviews_data)


    









import jieba
import collections
import re
import wordcloud 
import matplotlib.pyplot as plt


with open('comment_con_巴拉巴拉_cleaned.csv') as f:
    data = f.read()

# 文本预处理  去除一些无用的字符   只提取出中文出来
new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
new_data = " ".join(new_data)

# 文本分词
seg_list_exact = jieba.cut(new_data, cut_all=True)
result_list = []

with open('中文stopwords.txt', encoding='utf-8') as f:
    con = f.readlines()
    stop_words = set()
    for i in con:
        i = i.replace("\n", "")   # 去掉读取每一行数据的\n
        stop_words.add(i)

for word in seg_list_exact:
    # 设置停用词并去除单个词
    if word not in stop_words and len(word) > 1:
        result_list.append(word)
print(result_list)


# 筛选后统计
word_counts = collections.Counter(result_list)
# 获取前100最高频的词
word_counts_top100 = word_counts.most_common(100)
print(word_counts_top100)

# 绘制词云
wc = wordcloud.WordCloud(
    background_color='black',  # 设置背景颜色  默认是black
    width=900, height=600,
    max_words=100,            # 词云显示的最大词语数量
    font_path='SimHei.ttf',   # 设置字体  显示中文
    max_font_size=110,         # 设置字体最大值
    min_font_size=10,         # 设置子图最小值
    random_state=10)           # 设置随机生成状态，即多少种配色方案)
my_cloud = wc.generate_from_frequencies(word_counts)

#my_cloud = WordCloud(
    #background_color='white',  # 设置背景颜色  默认是black
    #width=900, height=600,
    #max_words=100,            # 词云显示的最大词语数量
    #font_path='simhei.ttf',   # 设置字体  显示中文
    #max_font_size=99,         # 设置字体最大值
    #min_font_size=16,         # 设置子图最小值
    #random_state=50           # 设置随机生成状态，即多少种配色方案
#).generate_from_frequencies(word_counts)

# 显示生成的词云图片
plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
plt.axis('off')
plt.show()
my_cloud.to_file("巴拉巴拉.png")

