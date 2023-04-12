'''I am a doc.'''
import re
import index
import os
import shutil
import math
import flask
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
            if filtered_query.get(token) is None:
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
    '''I am a doc.'''
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
    term_tf = {}
    default_filename = os.getenv("INDEX_PATH", "inverted_index_1.txt")
    file_to_find = "index_server/index/inverted_index/" + default_filename
    for term, _ in filtered_query.items():
        tf_list = {}
        with open(file_to_find,'r',encoding='utf-8') as inverted_index_file:
            for line in inverted_index_file:
                term_read = line.split(" ")[0]
                if term == term_read:
                    #idf = line.split()[1]
                    #doc_count = (len(line.split()) - 2)/3 这个term出现在多少个file里
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
    may be can directly calculated tf-idf.'''
    file_to_find = "index_server/index/inverted_index/"+ os.getenv(
                    "INDEX_PATH", "inverted_index_1.txt"
                    )
    # print("file_to_find",file_to_find)
    d_vector_list = {}
    d_norm_list = {}
    idf_list = {} #{term: idf} 每个term都只有一个idf
    for doc in output_doc:
        for term,_ in filtered_query.items():
            with open(file_to_find,'r',encoding='utf-8') as inverted_index_file:
                for line in inverted_index_file:
                    term_read = line.split(" ")[0]
                    if term == term_read:
                        idf = line.split()[1]
                        idf_list[term] = idf
                        for i in range (len(line.split())):
                            if line.split()[i] == doc:
                                d_norm_list[doc] = line.split()[i+2]
            tf_list = term_tf[term]
            # print("term is", term, "tf_list is ", tf_list, "doc is ", doc)
            if d_vector_list.get(doc) is None:
                d_vector_list[doc] = [float(tf_list[doc])*float(idf)]
            else:
                d_vector_list[doc].append(float(tf_list[doc])*float(idf))
    return d_vector_list,idf_list,d_norm_list

def query_vector(filtered_query,idf_list):
    '''I am a doc.'''
    q_vector = []
    # print("filtered_query",filtered_query)
    # print("idf_list",idf_list)
    for term, count in filtered_query.items():
        # print(term, count,(idf_list[term]))
        if idf_list.get(term):
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
    '''I am a doc.'''
    normalized_q_vector = 0 # {term: normalization factor}
    norm_sum = 0
    for i in q_vector:
        norm_sum += float(i) ** 2
    normalized_q_vector = math.sqrt(norm_sum)
    return normalized_q_vector

def tf_idf_score(d_vector_list, normalized_q_vector, q_vector,d_norm_list):
    "Calculate tf_idf_score"
    tf_idf_s = {}
    for doc, _ in d_vector_list.items():
        score = dot_product(q_vector, d_vector_list[doc])
        score = score/(float(normalized_q_vector) * math.sqrt(float(d_norm_list[doc])))
        tf_idf_s[doc] = score
    # print(tf_idf_s)
    return tf_idf_s

def weighted_score(weight, tf_idf_s):
    '''I ma a doc.'''
    pagerank_rank = {}
    weighted_s = {}
    with open("index_server/index/pagerank.out", "r", encoding='utf-8') as pagerank:
        for line in pagerank:
            docid = line.split(",")[0]
            rank = line.split(",")[1]
            pagerank_rank[docid] = rank
    for doc, tfidf in tf_idf_s.items():
        weighted_s[doc] = float(
            float(weight) * float(pagerank_rank[doc])
            + float(1 - weight) * float(tfidf))
    return weighted_s

def final_result(weighted_s):
    '''I am a doc.'''
    result = []
    sorted_weighted_s = {
        k: v for k, v in sorted(weighted_s.items(),
        key=lambda item: item[1], reverse=True)
        }
    for doc, score in sorted_weighted_s.items():
        item = {}
        item["docid"] = int(doc)
        item["score"] = score
        result.append(item)
    # print(dict(result))
    return result
