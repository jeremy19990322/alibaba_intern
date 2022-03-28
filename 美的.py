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
    reviews_data.to_csv("curr_review_data_cleaned.csv",index=False, encoding='utf_8_sig')
    
    
    
    fenci_list = []
    with open('中文stopwords.txt', encoding='utf-8') as f:
        con = f.readlines()
        stop_words = set()
    for i in con:
        i = i.replace("\n", "")   # 去掉读取每一行数据的\n
        stop_words.add(i)
    # 设置停用词并去除单个词
        
    for i in reviews_data["content"]:
        fenci_list.append(jieba.lcut(i))
    fenci_df = pd.DataFrame()
    fenci_df["f"] = fenci_list
    for i in fenci_df['f']:
        for k in i:
            if k in stop_words or len(k) <= 1:
                i.remove(k)
    fenci_df.to_csv('fenci.csv')

    
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
    print(stop_words)
    df = pd.DataFrame()
    df_20 = pd.DataFrame()
    word_df_20 = pd.DataFrame()
    
    


# 筛选后统计
    word_counts = collections.Counter(result_list)
# 获取前100最高频的词
    word_counts_top100 = word_counts.most_common(100)

    word_counts_top20 = word_counts.most_common(20)
    word_list_top20 = []
    for word in word_counts_top20:
        word_list_top20.append(word[0])
    word_df_20['w'] = word_list_top20
    word_df_20.to_csv("word_list_20.csv")
    df["w"] = word_counts_top100
    df_20['w'] = word_counts_top20
    #print(df)
    #print(df_20)
    df.to_csv("word_counts.csv")
    df_20.to_csv("word_counts_top20.csv")
    #print(word_counts_top100)
    print(word_counts)
    


 #绘制词云
    #wc = wordcloud.WordCloud(
        #background_color='black',  # 设置背景颜色  默认是black
        #width=900, height=600,
        #max_words=100,            # 词云显示的最大词语数量
        #font_path='SimHei.ttf',   # 设置字体  显示中文
        ##max_font_size=110,         # 设置字体最大值
        #min_font_size=10,         # 设置子图最小值
        ##random_state=10)           # 设置随机生成状态，即多少种配色方案)
    #my_cloud = wc.generate_from_frequencies(word_counts)

# 显示生成的词云图片
    #plt.imshow(my_cloud, interpolation='bilinear')
# 显示设置词云图中无坐标轴
    #plt.axis('off')
    #plt.show()
    #my_cloud.to_file("wordcloud.png")


reviews_data = pd.read_table("comment_con 美的空调差评.csv", encoding='gbk')
word_cloud(reviews_data)

import re
#文本预处理
import jieba
#jieba.load_userdict('美的评论全部.txt')#自定义词典
stopword = [line.strip() for line in open('中文stopwords.txt',encoding= 'utf-8').readlines()] #简体中文停用词

fr = open('美的空调好评.txt','r',encoding= 'gbk')
con = [fr.readlines()]
'''
分词，并去掉特殊字符、词语
'''
fw = open('meidi_content_n.txt','w',encoding='utf-8')
for i in con[0]:
    #if len(i.decode('utf-8'))<=10:
    if len(i)<=10:
        pass
    else:
        w1 = i.split("。")#按句号分句
        for j in w1:
            w2 = re.sub(r'，|。|？|：|“|”|！','',j.strip())#去掉特殊字符
            #w1 = re.sub(name1,name2,w1) #实体对齐
            w3 = list(jieba.cut(w2))#分词
            w4 = [w for w in w3 if w not in stopword]#去掉停用词
            outstr = ''
            for word in w4:
                outstr +=word
                outstr +=' '
            fw.write(outstr.strip().encode('utf-8').decode())
            fw.write('\n')
fw.close()


with open('meidi_content.txt',encoding= 'utf-8') as f1:
    data1 = f1.readlines()
with open('meidi_content.txt',encoding= 'utf-8') as f2:
    data2 = f2.read()

#社交网络关系（共现矩阵）
f2 = open('meidi_content.txt','r',encoding= 'utf-8')
word = f2.readlines()
name = data1
#name = data1[1:]
#总人数
wordcount = len(name) 

#初始化128*128值全为0的共现矩阵
cormatrix = [[0 for col in range(wordcount)] for row in range(wordcount)] 
#遍历矩阵行和列  
for colindex in range(wordcount):
    for rowindex in range(wordcount):
        cornum = 0
        #如果两个人名字在同一句话里出现，那么共现矩阵中两个人对应的值加1
        for originline in word:
            if name[colindex].strip() in originline and name[rowindex].strip() in originline:
                cornum += 1
        cormatrix[colindex][rowindex] = cornum

cor_matrix = np.matrix(cormatrix)
for i in range(len(name)):
    cor_matrix[i,i] = 0
social_cor_matrix = pd.DataFrame(cor_matrix, index = name,columns = name)
#把共现矩阵存进excel
social_cor_matrix.to_csv('social_cor_matrix.csv')

social_contact = pd.DataFrame(columns = ['name1','name2','frequency'])
#共现频率
for i in range(0,len(name)):
    for j in range(0,len(name)):
        if i<j and cormatrix[i][j] > 0:
            social_contact.loc[len(social_contact),'name1'] = name[i]
            social_contact.loc[len(social_contact)-1,'name2'] = name[j]
            social_contact.loc[len(social_contact)-1,'frequency'] = cormatrix[i][j]

social_contact.to_excel('social_contact.xlsx',index = False)
 

import pandas as pd

df = pd.DataFrame()

f = open('美的全部评论分词.txt','r',encoding= 'utf-8')
word = f.readlines()
df['c'] = word
df.to_excel('chaping.xlsx')

import jieba.posseg as pseg
import pandas as pd

data = pd.read_csv('curr_review_data_cleaned.csv')
lst = []
new_lst = []
for words in data['content']:
    cut = pseg.cut(words)
    for word, flag in cut:
        lst.append('%s %s' % (word, flag))

df = pd.DataFrame()
df['c'] = lst
df.to_csv('词性.csv', encoding='gbk')




import matplotlib.pyplot as plt
import numpy
from wordcloud import WordCloud
import collections
import jieba.posseg as pseg
import pandas as pd
import os

data = pd.read_csv('curr_review_data_cleaned.csv')
lst = []
for i in data['content']:
    word = pseg.cut(i)
    lst = lst + ([x.word for x in word if x.flag == 'l'])
df = pd.DataFrame()
df['content'] = lst
df.to_csv('名词.csv', encoding='gbk')
print(lst)
word_counts = collections.Counter(lst)
print(word_counts)


from matplotlib import colors


#建立颜色数组，可更改颜色
color_list=['#CD933F']

#调用
colormap=colors.ListedColormap(color_list)

wordcloud = WordCloud(font_path="SimHei.ttf",background_color="white",width=1000,height=880,mode="RGBA", colormap=colormap).generate_from_frequencies(word_counts)


plt.imshow(wordcloud,interpolation="bilinear")

plt.axis("off")

plt.show()

wordcloud.to_file("bg3.png")#生成的词云图片


import pandas as pd
import numpy as np
import jieba

data = pd.read_csv('comment_con 美的空调差评.csv', encoding='gbk')

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

data['cut_content'] = data.content.apply(chinese_word_cut)


from snownlp import SnowNLP



# result 0.8623218777387431 0.21406279508712744
def snow_sentiments(coment):
    s = SnowNLP(coment)
    return s.sentiments

data['sentiments'] = data.content.apply(snow_sentiments)

def snow_result(comemnt):
    s = SnowNLP(comemnt)
    if s.sentiments >= 0.6:
        return 1
    else:
        return 0


data['snlp_result'] = data.content.apply(snow_result)
data.to_csv("好评情感分析.csv", encoding='gbk')

