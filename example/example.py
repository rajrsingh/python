import os
import json

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# locally stores the list of words
all_words = []


@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; makes a JSON word/definition object, adds it to the list
def handle_words():
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    all_words.append(new_word)
    return ('', 204)


@app.route('/words', methods=['GET'])
# makes JSON from the list of all words.
def display_find(name=None):
    return json.dumps(all_words)


if __name__ == "__main__":
    app.run()
