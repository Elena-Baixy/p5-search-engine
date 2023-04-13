"""
Insta485 index (main) view.

URLs include:
/
"""
import threading
import heapq
import sqlite3
import flask
import requests
import search


# for index.html
@search.app.route('/', methods=['GET'])
def search_result():
    """Render the html."""
    # Get the query and weight from the index.html
    if (flask.request.args.get('q') is None
       or flask.request.args.get('q') == ""):
        return flask.render_template("index.html")
    query = flask.request.args.get('q', '')
    weight = flask.request.args.get('w', '')

    if query:
        if weight:
            results = get_search_results(query, weight)
        else:
            results = get_search_results(query, weight=0.5)
    else:
        results = []

    return flask.render_template('searchresult.html',
                                 query=query, weight=weight, results=results)


def get_search_results(query, weight):
    """Get the data from index server and do a little processing."""
    results_list = []
    threads = []

    # Create threads for concurrent requests
    for url in search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        threa = threading.Thread(target=fetch_results,
                                 args=(url, query, weight, results_list))
        threa.start()
        threads.append(threa)

    # Wait for all threads to finish
    for threa in threads:
        threa.join()

    # Merge the results from different Index servers
    merged_results = heapq.merge(*results_list,
                                 key=lambda x: x["score"], reverse=True)

    # Get the top 10 results (only docid and score)
    top_results = list(merged_results)[:10]

    # Get the actual information
    processed_result = process_result(top_results)

    return processed_result


def fetch_results(url, query, weight, results_list):
    """Call the index_server_url to get the results."""
    if weight:
        response = requests.get(f"{url}?q={query}&w={weight}",
                                timeout=1000)
    else:
        response = requests.get(f"{url}?q={query}",
                                timeout=1000)
    if response.status_code == 200:
        results_list.append(response.json()["hits"])


def process_result(top_results):
    """Use docid to get the title, url, and summary."""
    final_result = []
    conn = sqlite3.connect(search.app.config['DATABASE_FILENAME'])
    cursor = conn.cursor()
    for result in top_results:
        docid = result['docid']
        cursor.execute("SELECT docid, title, summary, "
                       "url FROM documents WHERE docid == ?", (docid, ))
        info_results = cursor.fetchall()
        json_results = [{"title": row[1],
                         "summary": row[2],
                         "url": row[3]} for row in info_results]
        final_result.extend(json_results)

    return final_result
