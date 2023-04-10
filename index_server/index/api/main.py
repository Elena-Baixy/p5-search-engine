import flask
import re
import index
import os
from flask import Flask

# Tips: 没有交集则要return no search result
# 若出现两遍相同词汇则frequency增加，而不是增加term

def load_index():
    stopwords_list =[]
    filtered_query = []
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)

    query = flask.request.args.get("q")
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.replace("  "," ")
    query = query.casefold()
    query = query.strip()
    tokens = query.split(" ")
    for token in tokens:
        if token not in stopwords_list:
            filtered_query.append(token)

    inverted_index_0 = []
    with open("inverted_index/inverted_index_0.txt", "r") as stopwords:
        for line in inverted_index_0:
            line = line.replace("\n","")
            inverted_index_0.append(line)
 
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
    intersect_list ={} #docid:count 如果不是交集，那么count就不会等于term的个数
    output_doc = [] #交集里的docid
    term_tf = {} #term : {docid: tf} 用于在doc_vector里找 这个交集的docid的tf，for term -》 for output_doc
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
    '''Calculate doc vector. doc_list should be docid : term1:tf*idf, term2:... / docid
    This structure is complicated need to be changed
    may be can directly calculated tf-idf'''
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    file_to_find = "index_server/index/inverted_index/" + default_filename
    d_vector_list = {}
    idf_list = {} #{term: idf} 每个term都只有一个idf
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
        q_vector_list[term] = count*float(idf_list[term]) #query的frequency * idf
    return q_vector_list
                
def dot_product(vec1,vec2):
    """Calculate dot product."""
    if len(vec1) != len(vec2):
        return 0
    return sum(float(i[0]) * float(i[1]) for i in zip(vec1, vec2))



# ...

# from flask import Flask
# import flask
# import re
# import index

# # import index.api  # noqa: E402  pylint: disable=wrong-import-position

# # Load inverted index, stopwords, and pagerank into memory
# # index.api.load_index()


# @index.app.route('/api/v1/')
# def get_service():
#     """Get all service."""
#     context ={
#     "hits": "/api/v1/hits/",
#     "url": "/api/v1/"
#     }
#     return flask.jsonify(**context)


# @index.app.route('/api/v1/hits/')
# def get_doc_hits():
#     # index.api.load_index()
#     stopwords_list =[]
#     filtered_query = {} #key 是一个query term value是 她的count
#     pagerank = {}
#     with open("stopwords.txt", "r") as stopwords:
#         for line in stopwords:
#             line = line.replace("\n","")
#             stopwords_list.append(line)
    
#     with open("pagerank.out", "r") as pagerank:
#         for line in pagerank:
#             docid, rank = line.split()
#             pagerank[docid] = rank

#     #这里读inverted_index 我没怎么看懂spec到底想让我们只读一个inverted_index_0/1/2.txt还是要全读再拼起来
#     #所以这里不对哈哈哈
#     inverted_index_0 = []
#     with open("inverted_index/inverted_index_0.txt", "r") as stopwords:
#         for line in inverted_index_0:
#             line = line.replace("\n","")
#             inverted_index_0.append(line)

#     query = flask.request.args.get("q")
#     query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
#     query = query.replace("  "," ")
#     query = query.casefold()
#     query = query.strip()
#     tokens = query.split(" ")
#     for token in tokens:
#         if token not in stopwords_list:
#             if token in filtered_query:
#                 filtered_query[token] +=1
#             else:
#                 filtered_query[token] =1
    
#     #doctfnorm_terms： {docid1 :[(term1,tf,idf,norm),(term2,tf,idf,norm).. ],
#     #                   docid2 :[(term1,tf,idf,norm),(term2,tf,idf,norm).. ], }
#     doctfnorm_terms = {}
#     for query_word in filtered_query:
#         for inverted_index in inverted_index_0:
#             term = inverted_index.split()[0]
            
#             if (query_word == term): #found the query word match a term in inverted index
#                 idf = inverted_index.split()[1]
#                 for i in range(2,len(inverted_index.split() - 1, 3)):
#                     docid = inverted_index.split()[i]
#                     tf = inverted_index.split()[i+1]
#                     norm = inverted_index.split()[i+2]
#                     if (docid not in doctfnorm_terms):
#                         doctfnorm_terms[docid] = [(term,tf,idf,norm)]
#                     elif docid in doctfnorm_terms:
#                         doctfnorm_terms[docid].append((term,tf,idf,norm))

#     #intersection : (term1: [(docid1,tf,idf,norm), (docid2,tf,idf,norm), ]
#     #               term2:  [(docid1,tf,idf,norm), (docid2,tf,idf,norm), ]
#     intersection = {}
#     for key, value in  doctfnorm_terms.items():
#         # this means one docid has all terms in query terms, so this docid 符合要求要留下
#         if len(value) == len(list(filtered_query.keys())):
#             for v in value:
#                 if v[0] not in intersection:
#                     intersection[v[0]] = [(key,v[1],v[2],v[3])]
#                 else:
#                     intersection[v[0]].append(key,v[1],v[2],v[3])


#     #query_vector: [(term1,qterm_tfidf),...]
#     query_vector = []
#     for term,tf in filtered_query.items():
#         #  term frequency in query * inverse document frequency.
#         qterm_tfidf = tf * intersection[term][0][2]
#         query_vector.append((term,qterm_tfidf))
    

#     # document_dict = {docid1: [tfi1 * idf, tfi1 * idf], docid2: [tfi1 * idf] }
#     document_dict = {}
#     for docid in doctfnorm_terms.keys():
#         document_vector = []
#         for query in query_vector:
#             term = query[0]
#             idf = intersection[term][0][2]
#             dtf = doctfnorm_terms[docid][1]
#             dterm_tfidf = idf * dtf
#             document_vector.append(dterm_tfidf)
        
#         document_dict[docid] = document_vector

#     for docid, document_vector in document_dict.items():
#         dot_prod = 0
#         for i in range (len(query_vector)):
#             dot_prod += query_vector[i][1] * document_vector[i]

