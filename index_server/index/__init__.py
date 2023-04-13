"""Copied from project2, need to change later."""
import os
import flask
# import index.api
app = flask.Flask(__name__)
import index.api  # noqa: E402  pylint: disable=wrong-import-position
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
