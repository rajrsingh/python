from flask import Flask
from flask import render_template
from flask import request

import os
from urllib.parse import urlparse
import json

import redis

app = Flask(__name__)

# connection string and initialization
COMPOSE_REDIS_URL = os.environ['COMPOSE_REDIS_URL']
parsed = urlparse(COMPOSE_REDIS_URL)
r = redis.StrictRedis(
    host=parsed.hostname,
    port=parsed.port,
    password=parsed.password,
    decode_responses=True)


@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into a hash
def handle_words(name=None):
    r.hset("words", request.form['word'], request.form['definition'])
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the hash, lists keys/values, zips keys/values, returns as json for display on the page.
def display_find(name=None):
    cursor_obj = r.hgetall('words')

    keys_list = list(cursor_obj.keys())
    values_list = list(cursor_obj.values())

    results_list = [{'word': word, 'definition': definition} for word, definition in zip(keys_list, values_list)]
    return json.dumps(results_list)

if __name__ == "__main__":
    app.run()
