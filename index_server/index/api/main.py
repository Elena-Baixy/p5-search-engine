import flask
import re
import index
import os
from flask import Flask

# Tips: 没有交集则要return no search result
# 若出现两遍相同词汇则frequency增加，而不是增加term
 
def query_cleaning(query):
    '''Load index and clean.'''
    stopwords_list =[]
    filtered_query = {}
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.replace("  "," ")
    query = query.casefold()
    query = query.strip()
    tokens = query.split(" ")
    for token in tokens: #count tokens in query
        if token not in stopwords_list:
            if filtered_query.get(token):
                filtered_query[token] = 1
            else:
                filtered_query[token] += 1
    return filtered_query

@index.app.route('/api/v1/')
def get_service():
    """Get all service."""
    context ={
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context),200

@index.app.route('/api/v1/hits/')
def get_doc_hits():
    query = flask.request.args.get("q")
    filtered_query = query_cleaning(query)
    output_doc, term_tf = find_doc(filtered_query)
    doc_vector(filtered_query,output_doc,term_tf)

def find_doc(filtered_query):
    '''Find the doc that containes the query.'''
    intersect_list ={}
    output_doc = []
    term_tf = {}
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    file_to_find = "index_server/index/inverted_index/" + default_filename
    for (term,count) in filtered_query:
        tf_list = {}
        with open(file_to_find,'r') as inverted_index_file:
            for line in inverted_index_file:
                term_read = line.split(" ")[0]
                if (term == term_read):
                    idf = line.split()[1]
                    doc_count = (len(line.split()) - 2)/3 #这个term出现在多少个file里
                    for i in range(2,len(line.split() - 1), 3):
                        if intersect_list.get(line.split()[i]):
                            intersect_list[line.split()[i]] += 1
                        else:
                            intersect_list[line.split()[i]] = 1
                            tf_list[[line.split()[i]]] = line.split()[i+1]
        
        term_tf[term] = tf_list
    for doc,count_doc in intersect_list.items():
        if doc == len(filtered_query):
            output_doc.append(doc)
    return output_doc,term_tf
    
def doc_vector(filtered_query,output_doc,term_tf):
    '''calculated query vector'''
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    file_to_find = "index_server/index/inverted_index/" + default_filename
    d_vector_list = {}
    idf_list = {}
    for doc in output_doc:
        for (term,count) in filtered_query:
            with open(file_to_find,'r') as inverted_index_file:
                for line in inverted_index_file:
                    term_read = line.split(" ")[0]
                    if (term == term_read):
                        idf = line.split()[1]
                        idf_list[term] = idf
            for tf_list in term_tf[term]:
                d_vector_list[doc] += float(tf_list[doc])*float(idf)
    return d_vector_list,idf_list

def query_vector(filtered_query,idf_list):
    q_vector_list = {}
    for (term,count) in filtered_query:
        q_vector_list[term] = count*float(idf_list[term])
    return q_vector_list
                



    

