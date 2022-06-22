#!/usr/bin/env python
# coding: utf-8

import ltp
from ltp import LTP


ltp = LTP()
properties = ['药物成分','药物剂型','药物性味','中药功效','症状','疾病','人群','食物','食物分组']


def formulate(word):#把问句中提取出的关键词与json数据中的变量名进行匹配(可能是近义词)
    for i in ['成分', '成份', '化学成分', '有效成分', '组分']:
        if word == i:
            return '药物成分'
    for i in ['剂型', '复方', '处方', '片剂', '制剂']:
        if word == i:
            return '药物剂型'
    for i in ['性味', '性温', '性寒', '滋阴', '性平', '健脾', '味苦', '益气健', '补气', '全草']:
        if word == i:
            return '药物性味'
    for i in ['功效', '疗效', '功用']:
        if word == i:
            return '中药功效'
    for i in ['症状', '病症', '病征', '征状', '并发症']:
        if word == i:
            return '症状'
    for i in ['疾病', '病症', '并发症', '传染病', '慢性病']:
        if word == i:
            return '疾病'
    if word == "病":
            return '疾病'
    elif word == "人":
        return '人群'
    elif word == "饮食禁忌" or word == "饮食":
        return '食物分组'
    elif word == "忌口":
        return '食物分组'
    elif word == "味道":
        return '药物性味'
    elif word == "信息":
        return 'text'
    else:
        return word

def find(s, a):#匹配词性表中是否有相符的词性
    for index,value in enumerate(a):
        if(s == value):
            return index+1#为了避开0所以加一
    else:
        return 0


def correct(words,flags):
    for index,value in enumerate(words):
        if(words[index][0]=='吃' and words[index]!='吃'):
            w=words[index]
            words.insert(index,'吃')
            w=w[1:]
            words.insert(index+1,w)
            words.remove(value)
            flags.insert(index+1,'n')

    
    
def hasMedName(flags,words):
    nz = find('nz',flags)
    nh = find('nh',flags)
    ns = find('ns',flags)
    if(nz!=0):i=nz
    elif(nh!=0):i=nh
    else:i=ns
    #print(i)
    if find('r',flags):#问句中是否有“哪些”“哪种”“什么”之类的提示词（这样的词后面一般有关键词）
        #print(find('r',flags))
        #print( words[i-1],formulate(words[find('r',flags)]))
        return words[i-1],formulate(words[find('r',flags)])
    #如果没有疑问代词，那么问句中其他的名词或形容词可能就是关键词
    elif find('n',flags):
        return words[i-1],formulate(words[find('n',flags)-1])
    elif find('a',flags):
        return words[i-1],formulate(words[find('a',flags)-1])
    #“能”或“可以”这样的提示词后面往往是动词，但也是关键词
    elif find('能',words):
        if(flags[0]=='v'):#感冒能吃阿司匹林吗？
            return words[i-1],words[0]
        return words[i-1],words[find('能',words)]
    elif find('可以',words):
        if(flags[0]=='v'):
            return words[i-1],words[0]
        return words[i-1],words[find('可以',words)]#阿司匹林可以抗炎吗？
    elif flags[0]=='v':
        return words[i-1],words[0]
    else:#如果只找到药物名，就只返回药物名
        return words[i-1]   

    
def parse_query(querystring):
    ltp.init_dict(path="medicals_name.txt", max_window=5)
    seg, hidden = ltp.seg([querystring])
    #print(seg)
    pos = ltp.pos(hidden)
    #print(pos)
    print("分词结果为：")
    words = seg[0]
    flags = pos[0]
    correct(words,flags)
    # print(words, flags)
    # 处理偏正结构问句
    if flags[1] == 'u':
        if flags[2]=='n':
            return words[0], words[2]
        else:
            return words[0], words[3]
    #处理动宾结构问句
    if find('nz',flags) or find('nh',flags) or find('ns',flags):#问句中有具体的药物名
        return(hasMedName(flags,words))
    if find('r',flags): 
        if words[0]!='吃' and words[0]!='有' and flags[0]=='v' or flags[0]=='n':#感冒能吃什么药？妇科病能吃什么药？
            return words[0]
    if find('n',flags):
        if words[find('n',flags)-1]=="药":
            for index in range(find('n',flags),len(words)):#从“药”的下一个开始找
                #print(index)
                if flags[index]=='n':#句中有实名词（除“药”这样模糊的）
                    return words[index]
        else:
            for index in range(find('n',flags),len(words)):#从找到实名词的下一个开始找
                #print(index)
                if flags[index]=='n':
                    return words[index],words[find('n',flags)-1]
    if find('a',flags):
            return formulate(words[find('a',flags)-1])
    if find('能',words):
            return words[find('能',words)]
    if find('可以',words):
            return words[find('可以',words)]
    else:
        return 0
            

if __name__ == "__main__":
    print(parse_query('哪些药含有麝香？'))
    print(parse_query('哪些药是含有水泥的？'))

    print(parse_query('乌鸡白凤丸含有乌鸡吗？'))
    print(parse_query('乌鸡白凤丸含有凤凰吗？'))
    
    print(parse_query('八珍益母丸的药物成分有哪些？'))
    print(parse_query('哪些症状可以吃乌鸡白凤丸？'))
    print(parse_query('大力丸的药物成分有哪些？'))
