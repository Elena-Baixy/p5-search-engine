"""Copied from project2, need to change later"""
import os
import index.inverted_index
import index.loader
import flask
app = flask.Flask(__name__)
from index import api
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
# import index.pagerank
# import index.stopwords
