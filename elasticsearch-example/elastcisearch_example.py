from flask import Flask
from flask import render_template
from flask import request

from elasticsearch import Elasticsearch

import os
import certifi
from urllib.parse import urlparse
import json


app = Flask(__name__)

# connection string and initialization
COMPOSE_ELASTICSEARCH_URL = os.environ['COMPOSE_ELASTICSEARCH_URL']
parsed = urlparse(COMPOSE_ELASTICSEARCH_URL)

es = Elasticsearch(
    [parsed.hostname],
    http_auth = (parsed.username, parsed.password),
    port = parsed.port,
    use_ssl = True,
    verify_certs = True
)


@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into index, refreshes index
def handle_words(name=None):
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    es.index(index="words", doc_type="word", body=new_word)
    es.indices.refresh(index="words")
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the index, returns as json for display on the page.
def display_find(name=None):
    res = es.search(index="words", doc_type="word", body={})
    hit_list = (res['hits']['hits'])

    words_list = []
    for hit in hit_list:
        words_list.append(hit['_source'])

    return json.dumps(words_list)

if __name__ == "__main__":
    app.run()
