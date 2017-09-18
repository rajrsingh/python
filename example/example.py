import os
import json

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; makes a JSON word/definition object.
def handle_words(name=None):
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the collection, returns as json for display on the page.
def display_find(name=None):
    all_words = []
    return json.dumps(all_words)


if __name__ == "__main__":
    app.run()
