from flask import Flask
from flask import render_template
from flask import request

import os
from urllib.parse import urlparse
import json

import rethinkdb as r

app = Flask(__name__)

# connection string and initialization
compose_rethinkdb_url = os.environ['COMPOSE_RETHINKDB_URL']
path_to_rethinkdb_cert = os.environ['PATH_TO_RETHINKDB_CERT']

parsed = urlparse(compose_rethinkdb_url)
conn = r.connect(
    host=parsed.hostname,
    port=parsed.port,
    user=parsed.username,
    password=parsed.password,
    ssl={'ca_certs': path_to_rethinkdb_cert}
   )


try:
    r.db_create('grand_tour').run(conn)
    conn.use("grand_tour")
    r.table_create('words',shards=1,replicas=3).run(conn)
except r.ReqlRuntimeError:
    # assume database or table already exists
    pass

conn.use("grand_tour")

@app.route('/')
# top-level page display
def serve_page(name=None):
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into table
def handle_words(name=None):
    new_word = {"word":request.form['word'], "definition":request.form['definition']}
    r.table("words").insert(new_word).run(conn)
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the table, returns as json for display on the page.
def display_find(name=None):
    cursor_obj = r.table("words").pluck("word", "definition").run(conn)
    word_list = list(cursor_obj)
    return json.dumps(word_list)

if __name__ == "__main__":
    app.run()
