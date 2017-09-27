import os
import ssl
from urllib.parse import urlparse
import uuid
import json

from flask import Flask
from flask import render_template
from flask import request

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


app = Flask(__name__)

# connection string and certificate path
compose_scylla_url = os.environ['COMPOSE_SCYLLA_URL']
path_to_scylla_cert = os.environ['PATH_TO_SCYLLA_CERT']
parsed = urlparse(compose_scylla_url)

# Optional dict with absolute path to CA certificate and the defualt Cassandra protocol ssl version.
ssl_options = {
    'ca_certs': path_to_scylla_cert,
    'ssl_version': ssl.PROTOCOL_TLSv1
}

# Creates class object that supplies username/password in plain-text.
auth_provider = PlainTextAuthProvider(
                username=parsed.username,
                password=parsed.password)

# Handles connection setup and information
cluster = Cluster(
            contact_points = [parsed.hostname],
            port = parsed.port,
            auth_provider = auth_provider,
            ssl_options=ssl_options)

# Starts session, connects to a keyspace
session = cluster.connect("grand_tour")


@app.route('/')
# top-level page display, starts session, connects to a keyspace
def serve_page(name=None):
    session.execute("""CREATE TABLE IF NOT EXISTS words (
		id UUID primary key,
		word text,
		definition text) """)
    return render_template('index.html', name=name)

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into table
def handle_words(name=None):

    new_word = session.prepare("""
    INSERT INTO words(id, word, definition)
    VALUES (?, ?, ?)""")

    session.execute(new_word, [uuid.uuid4(), request.form['word'], request.form['definition']])
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the table, returns as json for display on the page.
def display_find(name=None):
    get_words = session.execute("""SELECT word, definition FROM words""")
    
    word_list = []
    definition_list =[]
    
    for entry in get_words:
        word_list.append(entry[0])
        definition_list.append(entry[1])

    results_list = [{'word': word, 'definition': definition} for word, definition in zip(word_list, definition_list)]
             
    return json.dumps(results_list)

    
if __name__ == "__main__":
    app.run()
