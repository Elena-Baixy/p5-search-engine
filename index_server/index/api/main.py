# ...
from flask import Flask

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

@route('/api/v1/')
def get_service():
    """Get all service."""
    context ={
    "hits": "/api/v1/hits/",
    "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@route('/api/v1/hits/')
def get_doc_hits():
    # index.api.load_index()
    stopwords_list =[]
    filtered_query = []
    pagerank = {}
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)
    
    with open("pagerank.out", "r") as pagerank:
        for line in pagerank:
            docid, rank = line.split()
            pagerank[docid] = rank

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
            filtered_query.append(token)
    
    all_terms = []
    for word in filtered_query:
        for inverted_index in inverted_index_0:
            if (word == inverted_index.split()[0]):
                idf = inverted_index.split()[1]
                doc_count = (len(inverted_index.split()) - 2)/3
                doctfnorm_terms = []
                for i in range(2,len(inverted_index.split() - 1, 3):
                    docid = inverted_index.split()[i]
                    tf = inverted_index.split()[i+1]
                    norm = inverted_index.split()[i+2]
                    doctfnorm_terms.append((docid,tf,norm)))
            all_terms.append(doctfnorm_terms)
    
    intersection = set(doctfnorm_terms[0])
    for lst in all_docid[1:]:
        intersection.intersection_update(item1 for item1, item2 in lst)
    #TODO check intersection is empty



                



    

