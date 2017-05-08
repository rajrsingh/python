from flask import Flask
from flask import render_template
from flask import request

import os

import pymongo
from pymongo import MongoClient
import ssl
from bson import json_util

app = Flask(__name__)

# connection string and initialization
MONGODB_URL = os.environ['MONGODB_URL']
client = MongoClient(MONGODB_URL,ssl_cert_reqs=ssl.CERT_NONE)

# databse/collection names
db = client.grand_tour
collection = db.python

@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into collection
def handle_words(name=None):
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    doc_id = collection.insert_one(new_word).inserted_id
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the collection, returns as json for display on the page.
def display_find(name=None):
    cursor_obj = collection.find({},{"_id":0})
    return json_util.dumps(cursor_obj)

if __name__ == "__main__":
    app.run()
