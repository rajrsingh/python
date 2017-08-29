import os
import ssl

from flask import Flask
from flask import render_template
from flask import request

import pymongo
from pymongo import MongoClient

from bson import json_util


app = Flask(__name__)

# connection string and initialization
mongodb_url = os.environ['COMPOSE_MONGODB_URL']
path_to_cert = os.environ['PATH_TO_MONGODB_CERT']
client = MongoClient(
    mongodb_url, 
    ssl=True, 
    ssl_ca_certs=path_to_cert
)

# databse/collection names
db = client.grand_tour
collection = db.words

@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into collection
def handle_words():
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    doc_id = collection.insert_one(new_word).inserted_id
    return "ECHO: PUT\n"


@app.route('/words', methods=['GET'])
# query for all the words in the collection, returns as json for display on the page.
def display_find():
    cursor_obj = collection.find({}, {"_id":0})
    return json_util.dumps(cursor_obj)

if __name__ == "__main__":
    app.run()
