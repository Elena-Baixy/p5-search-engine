"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import uuid
import hashlib
import pathlib
import flask
from flask import send_from_directory
import arrow
import requests
import threading
import heapq
import search_server
import socket
import json
from queue import PriorityQueue


# for index.html
@search_server.app.route('/', methods=['GET'])
def search():
    # Get the query and weight from the index.html
    query = flask.request.args.get('q', '')
    weight = flask.request.args.get('w', '')

    if query:
        
        results = get_search_results(query, weight)
    else:
        results = []

    return flask.render_template('index.html', query=query, weight=weight, results=results)

def get_search_results(query, weight):
    "Get the data from index server and do a little processing"

    "Create a thread for each index server"
    results_queue = PriorityQueue()
    threads = []


    # Create threads for concurrent requests
    for url in SEARCH_INDEX_SEGMENT_API_URLS:
        t = threading.Thread(target=fetch_results, args=(url, query, weight, results_queue))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge the results from different Index servers
    merged_results = heapq.merge(*[results_queue.get() for _ in range(results_queue.qsize())], key=lambda x: x["score"], reverse=True)

    # Get the top 10 results
    top_results = list(merged_results)[:10]
    
    return top_results


def fetch_results(url, query, weight, results_queue):
    "call the index_server_url to get the results"
    if weight: 
        response = requests.get(f"{url}?q={query}&w={weight}")
    else: 
        response = requests.get(f"{url}?q={query}")
    if response.status_code == 200:
        results_queue.put(response.json()["hits"])
    return results_queue

    