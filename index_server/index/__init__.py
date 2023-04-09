# ...
from flask import Flask
import flask
import re
import index

# import index.api  # noqa: E402  pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
# index.api.load_index()

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

@index.app.route('/api/v1/')
def get_service():
    """Get all service."""
    context ={
    "hits": "/api/v1/hits/",
    "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/')
def get_doc_hits():
    # index.api.load_index()
    stopwords_list =[]
    filtered_query = {} #key 是一个query term value是 她的count
    pagerank = {}
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)
    
    with open("pagerank.out", "r") as pagerank:
        for line in pagerank:
            docid, rank = line.split()
            pagerank[docid] = rank

    #这里读inverted_index 我没怎么看懂spec到底想让我们只读一个inverted_index_0/1/2.txt还是要全读再拼起来
    #所以这里不对哈哈哈
    inverted_index_0 = []
    with open("inverted_index/inverted_index_0.txt", "r") as stopwords:
        for line in inverted_index_0:
            line = line.replace("\n","")
            inverted_index_0.append(line)

    query = flask.request.args.get("q")
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.replace("  "," ")
    query = query.casefold()
    query = query.strip()
    tokens = query.split(" ")
    for token in tokens:
        if token not in stopwords_list:
            if token in filtered_query:
                filtered_query[token] +=1
            else:
                filtered_query[token] =1
    
    #doctfnorm_terms： {docid1 :[(term1,tf,idf,norm),(term2,tf,idf,norm).. ],
    #                   docid2 :[(term1,tf,idf,norm),(term2,tf,idf,norm).. ], }
    doctfnorm_terms = {}
    for query_word in filtered_query:
        for inverted_index in inverted_index_0:
            term = inverted_index.split()[0]
            
            if (query_word == term): #found the query word match a term in inverted index
                idf = inverted_index.split()[1]
                for i in range(2,len(inverted_index.split() - 1, 3)):
                    docid = inverted_index.split()[i]
                    tf = inverted_index.split()[i+1]
                    norm = inverted_index.split()[i+2]
                    if (docid not in doctfnorm_terms):
                        doctfnorm_terms[docid] = [(term,tf,idf,norm)]
                    elif docid in doctfnorm_terms:
                        doctfnorm_terms[docid].append((term,tf,idf,norm))

    #intersection : (term1: [(docid1,tf,idf,norm), (docid2,tf,idf,norm), ]
    #               term2:  [(docid1,tf,idf,norm), (docid2,tf,idf,norm), ]
    intersection = {}
    for key, value in  doctfnorm_terms.items():
        # this means one docid has all terms in query terms, so this docid 符合要求要留下
        if len(value) == len(list(filtered_query.keys())):
            for v in value:
                if v[0] not in intersection:
                    intersection[v[0]] = [(key,v[1],v[2],v[3])]
                else:
                    intersection[v[0]].append(key,v[1],v[2],v[3])


    #query_vector: [(term1,qterm_tfidf),...]
    query_vector = []
    for term,tf in filtered_query.items():
        #  term frequency in query * inverse document frequency.
        qterm_tfidf = tf * intersection[term][0][2]
        query_vector.append((term,qterm_tfidf))
    

    # document_dict = {docid1: [tfi1 * idf, tfi1 * idf], docid2: [tfi1 * idf] }
    document_dict = {}
    for docid in doctfnorm_terms.keys():
        document_vector = []
        for query in query_vector:
            term = query[0]
            idf = intersection[term][0][2]
            dtf = doctfnorm_terms[docid][1]
            dterm_tfidf = idf * dtf
            document_vector.append(dterm_tfidf)
        
        document_dict[docid] = document_vector

    for docid, document_vector in document_dict.items():
        dot_prod = 0
        for i in range (len(query_vector)):
            dot_prod += query_vector[i][1] * document_vector[i]





    

    










                



    

