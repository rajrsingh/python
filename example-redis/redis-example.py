import os
from urllib.parse import urlparse
import json

from flask import Flask
from flask import render_template
from flask import request

import redis


app = Flask(__name__)


# connection string and initialization
compose_redis_url = os.environ['COMPOSE_REDIS_URL']

ssl_wanted=compose_redis_url.startswith("rediss:")
parsed = urlparse(compose_redis_url)
ssl_wanted=compose_redis_url.startswith("rediss:")
r = redis.StrictRedis(
    host=parsed.hostname,
    port=parsed.port,
    password=parsed.password,
    ssl=ssl_wanted,
    decode_responses=True)


@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into a hash
def handle_words():
    r.hset("words", request.form['word'], request.form['definition'])
    return ('', 204)


@app.route('/words', methods=['GET'])
# queries and formats results for display on page
def display_find():
    # query for all the words in the hash
    cursor_obj = r.hgetall('words')

    #makes two lists, one of keys and one of values
    keys_list = list(cursor_obj.keys())
    values_list = list(cursor_obj.values())

    # zips the lists of keys/values together, and makes an object of all word/definition pairs
    results_list = [{'word': word, 'definition': definition} 
        for word, definition in zip(keys_list, values_list)]
    
    # returns a json object from the object of word/definition pairs
    return json.dumps(results_list)


if __name__ == "__main__":
    app.run()
