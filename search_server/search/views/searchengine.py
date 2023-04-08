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
    
