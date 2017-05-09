from flask import Flask
from flask import render_template
from flask import request

import os
from urllib.parse import urlparse
import json

import psycopg2

app = Flask(__name__)

# connection string and db connection initialization
POSTGRESQL_URL = os.environ['POSTGRESQL_URL']
parsed = urlparse(POSTGRESQL_URL)
conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port,
    user=parsed.username,
    password=parsed.password,
    database='grand_tour')

@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into collection
def handle_words(name=None):
    cur = conn.cursor()
    cur.execute("""INSERT INTO python (word, definition)
        VALUES (%s, %s)""",(request.form['word'],request.form['definition']))
    conn.commit()
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the collection,\
# makes a dictionary object from the column names and the results,\
# makes json from the dict for display on the page.
def display_find(name=None):
    cur = conn.cursor()
    cur.execute("""SELECT word, definition FROM python""")

    cursor_obj = [dict
    ((cur.description[col][0], row) for col, row in enumerate(q_results))
    for q_results in cur.fetchall()]

    return json.dumps(cursor_obj)

if __name__ == "__main__":
    app.run()
