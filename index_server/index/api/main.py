import flask
import re
import index
import os
import shutil
import math
from flask import Flask

# Tips: 没有交集则要return no search result
# 若出现两遍相同词汇则frequency增加，而不是增加term

# load index似乎是把那些file放在正确的位置上,然后放在memory上，但是我不理解的是如果我们直接在每次用的时候再放在memory里不是会更好吗？
def load_index():
    "load the file into correct place"
    if not os.path.exists("index_server/index/stopwords.txt"):
        shutil.copyfile('inverted_index/stopwords.txt',
                        'index_server/index/stopwords.txt')
    inverted_index_folder = "index_server/index/inverted_index"
    if not os.path.exists("index_server/index/inverted_index"):
        os.mkdir(inverted_index_folder)

    # 这些暂时先comment掉说不定以后需要放回来
    # # 好像不需要check?
    # # if not os.path.exists("inverted_index/output"):
    # #     os.mkdir("inverted_index/output")
    # output_files = sorted(os.listdir("inverted_index/output"))
    # number = 0
    # for output_file in output_files:
    #     output_file_path = os.path.join("inverted_index/output", output_file)
    #     inverted_index_file = "inverted_index_" + str(number) + ".txt"
    #     shutil.copy(output_file_path, "index_server/index/inverted_index" + inverted_index_file)
    #     number += 1
    

 
def query_cleaning(query):
    '''Load index and clean.'''
    stopwords_list =[]
    filtered_query = {}
    with open("inverted_index/stopwords.txt", "r", encoding = 'utf-8') as stopwords:
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
            if filtered_query.get(token) == None:
                filtered_query[token] = 1
            else:
                filtered_query[token] += 1
    # print(filtered_query)
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
    weight = flask.request.args.get("w", default=0.5)
    filtered_query = query_cleaning(query)
    output_doc, term_tf = find_doc(filtered_query)
    d_vector_list, idf_list,d_norm_list = doc_vector(filtered_query,output_doc,term_tf)
    # print("d_vector_list-----",d_vector_list)
    # print("idf_list-----",idf_list)
    q_vector = query_vector(filtered_query,idf_list)
    # print("query_vector-----",q_vector)
    normalized_q_vector = normalized_q(q_vector)
    # print("normalized_q-----",normalized_q_vector)
    tf_idf_s = tf_idf_score(d_vector_list, normalized_q_vector, q_vector, d_norm_list)
    # print("tf_idf_score-----",tf_idf_s)
    weighted_s = weighted_score(float(weight), tf_idf_s)
    result = final_result(weighted_s)
    context = {}
    context["hits"] = result
    # print("result-----", result)
    return flask.jsonify(**context), 200


    
    

def find_doc(filtered_query):
    '''Find the doc that containes the query.'''
    intersect_list ={} #docid:count 如果不是交集，那么count就不会等于term的个数
    output_doc = [] #交集里的docid
    term_tf = {} #term : {docid: tf} 用于在doc_vector里找 这个交集的docid的tf，for term -》 for output_doc
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    file_to_find = "index_server/index/inverted_index/" + default_filename
    for term, count in filtered_query.items():
        tf_list = {}
        with open(file_to_find,'r') as inverted_index_file:
            for line in inverted_index_file:
                term_read = line.split(" ")[0]

                if (term == term_read):

                    # print("term_read", term_read)
                    idf = line.split()[1]
                    doc_count = (len(line.split()) - 2)/3 #这个term出现在多少个file里
                    for i in range(2,len(line.split()) - 1, 3):
                        if intersect_list.get(line.split()[i]):
                            intersect_list[line.split()[i]] += 1
                            tf_list[line.split()[i]] = line.split()[i+1]
                            # print("tf_list", tf_list)
                        else:
                            intersect_list[line.split()[i]] = 1
                            tf_list[line.split()[i]] = line.split()[i+1]
        term_tf[term] = tf_list
    for doc,count_doc in intersect_list.items():
        if count_doc == len(filtered_query):
            output_doc.append(doc)
    # print("output_doc", output_doc)
    # print("term_tf", term_tf)
    # print("intersect_list",intersect_list)
    return output_doc,term_tf
    
def doc_vector(filtered_query,output_doc,term_tf):
    '''Calculate doc vector. doc_list should be docid : term1:tf*idf, term2:... / docid
    This structure is complicated need to be changed
    may be can directly calculated tf-idf'''
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    # TODO: changeback!!!!
    file_to_find = "index_server/index/inverted_index/" + default_filename
    # print("file_to_find",file_to_find)
    d_vector_list = {}
    d_norm_list = {}
    idf_list = {} #{term: idf} 每个term都只有一个idf
    for doc in output_doc:
        for term,count in filtered_query.items():
            with open(file_to_find,'r') as inverted_index_file:
                for line in inverted_index_file:
                    term_read = line.split(" ")[0]
                    if (term == term_read):
                        idf = line.split()[1]
                        idf_list[term] = idf
                        for i in range (len(line.split())):
                            if line.split()[i] == doc:
                                d_norm_list[doc] = line.split()[i+2]
                        
            tf_list = term_tf[term]
            # print("term is", term, "tf_list is ", tf_list, "doc is ", doc)
            if d_vector_list.get(doc) == None:
                d_vector_list[doc] = [float(tf_list[doc])*float(idf)]
                
            else: 
                d_vector_list[doc].append(float(tf_list[doc])*float(idf))
           
    # print("d_norm_list",d_norm_list)
    # print("d_vector_list", d_vector_list)
    # print("idf_list", idf_list)
    return d_vector_list,idf_list,d_norm_list

def query_vector(filtered_query,idf_list):
    q_vector = []
    # print("filtered_query",filtered_query)
    # print("idf_list",idf_list)
    for term, count in filtered_query.items():
        # print(term, count,(idf_list[term]))
        if (idf_list.get(term)):
            result = count * float(idf_list[term])
            q_vector.append(result)
    # print("q_vector",q_vector)
    return q_vector
                
def dot_product(vec1,vec2):
    """Calculate dot product."""
    if len(vec1) != len(vec2):
        return 0
    return sum(float(i[0]) * float(i[1]) for i in zip(vec1, vec2))

def normalized_q(q_vector):
    normalized_q_vector = 0 # {term: normalization factor}
    sum = 0
    for i in q_vector:
        sum += float(i) ** 2
    normalized_q_vector = math.sqrt(sum)
    return normalized_q_vector

def tf_idf_score(d_vector_list, normalized_q_vector, q_vector,d_norm_list):
    "Calculate tf_idf_score"
    normalized_d_vectors = {} # {term: normalization factor}

    # for doc, d_vector in d_vector_list.items():
    #     sum = 0
    #     for i in d_vector:
    #         sum += float(i) ** 2
    #     normalized_d_vectors[doc] = math.sqrt(sum)
    # final tf_idf score:
    tf_idf_s = {} 
    for doc, d_vector in d_vector_list.items():
        score = dot_product(q_vector, d_vector_list[doc])
        score = score/(float(normalized_q_vector) * math.sqrt(float(d_norm_list[doc])))
        tf_idf_s[doc] = score
    # print(tf_idf_s)
    return tf_idf_s

def weighted_score(weight, tf_idf_s):
    pagerank_rank = {}
    weighted_s = {}
    with open("index_server/index/pagerank.out", "r", encoding='utf-8') as pagerank:
        for line in pagerank:
            docid = line.split(",")[0]
            rank = line.split(",")[1]
            pagerank_rank[docid] = rank
    for doc, tfidf in tf_idf_s.items():
        weighted_s[doc] = float(float(weight) * float(pagerank_rank[doc]) + float(1 - weight) * float(tfidf))
    return weighted_s

def final_result(weighted_s):
    result = []
    sorted_weighted_s = {k: v for k, v in sorted(weighted_s.items(), key=lambda item: item[1], reverse=True)}
    for doc, score in sorted_weighted_s.items():
        item = {}
        item["docid"] = int(doc)
        item["score"] = score
        result.append(item)
    # print(dict(result))
    return result









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

