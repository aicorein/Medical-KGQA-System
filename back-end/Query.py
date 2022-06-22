#!/usr/bin/env python
# coding: utf-8

from SPARQLWrapper import SPARQLWrapper, JSON
import json
from queryProcess import processData
from parseQuery import parse_query


sparql = SPARQLWrapper("http://localhost:3030/medicals/")#这里要改现在的项目
head=    """prefix : <https://example.org/rules/>  
            prefix blcu: <http://www.blcu.edu.cn/ontology#>  
            prefix dbo: <http://dbpedia.org/ontology/>  
            prefix ql: <http://semweb.mmlab.be/ns/ql#>  
            prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
            prefix rml: <http://semweb.mmlab.be/ns/rml#>  
            prefix rr: <http://www.w3.org/ns/r2rml#>  
            prefix schema: <http://schema.org/>"""
pred_list = ['药物成分','药物剂型','药物性味','中药功效','症状',
        '人群','食物分组','食物','疾病','证候','疾病分组','药品分组',]


def getResult(query_string):#查询一下试试有木有结果
    try:
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        # print(query_string)
        return results
    except Exception:
        return False


def to_sparql(*a): 
    #参数可能有一个或两个
    if len(a)==0:
        return "no effective query"
    elif len(a)==1:
        # 保存状态
        state = 0

        a=str(a)
        a=a.split("\'")[1]
        #一个参数可能是药品名或object
        statements=["?sub blcu:国药准字 ?number.\n ?sub ?pred blcu:"+a+".",#是object，什么药含有麝香？
                    ]#是subject，过敏体质者慎服什么药
        for i in range(1):
            state += 1
            statement=statements[i]
            # print(statement)
            query_string = head+"""
            SELECT * WHERE {
            """+statement+"""
            } 
            """
            res = getResult(query_string)
            if(res and len(res['results']['bindings']) != 0):
                return res, state
        return False, state
    else:
        state = 1
        #两个参数时，其中一个一定是subject，剩下的可能是predicate或object，共四种情况
        statements=["?sub blcu:国药准字 ?number.\n ?sub blcu:药品  blcu:"+a[0]+".\n\t?sub ?pred blcu:"+a[1]+".",
                    "?sub blcu:国药准字 ?number.\n ?sub blcu:药品  blcu:"+a[0]+".\n\t?sub blcu:"+a[1]+" ?obj."]
        for i in range(2):
            state += 1
            statement=statements[i]
            # print(statement)
            query_string = head+"""
            SELECT * WHERE {
            """+statement+"""
            } 
            """
            res = getResult(query_string)
            if res and len(res['results']['bindings']) != 0: 
                return res, state
        return False, state


def query(query_string):
    key_words = parse_query(query_string)
    # key_words = '麝香'
    if isinstance(key_words, str): key_words = (key_words, )
    if len(key_words[-1]) > len(key_words[0]) and not (key_words[0] in pred_list or key_words[-1] in pred_list):
        key_words = tuple(reversed(key_words))

    print(key_words)
    result, state = to_sparql(*key_words)
    if result == False and state == 3 and key_words[-1] not in pred_list:
        state = 2
    result = processData(key_words, result, state)
    return result


if __name__ == "__main__":
    query('哪些药含有麝香')