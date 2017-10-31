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

# connection strings, parsing, and certificate path
compose_scylla_url = os.environ['COMPOSE_SCYLLA_URL']
url1,url2,url3 = compose_scylla_url.split(",")

cstr1 = urlparse(url1)
cstr2 = urlparse(url2)
cstr3 = urlparse(url3)

path_to_scylla_cert = os.environ['PATH_TO_SCYLLA_CERT']

# Optional dict with absolute path to CA certificate and the defualt Cassandra protocol ssl version.
ssl_options = {
    'ca_certs': path_to_scylla_cert,
    'ssl_version': ssl.PROTOCOL_TLSv1
}

# Creates class object that supplies username/password in plain-text.
auth_provider = PlainTextAuthProvider(
                username=cstr1.username,
                password=cstr1.password)

# Handles connection setup and information
cluster = Cluster(
            contact_points = [cstr1.hostname,cstr2.hostname,cstr3.hostname],
            port = cstr1.port,
            auth_provider = auth_provider,
            ssl_options=ssl_options)

# Starts session, connects to a keyspace
session = cluster.connect("grand_tour")

@app.route('/')
# top-level page display, creates table on first run
def serve_page():
    session.execute("""CREATE TABLE IF NOT EXISTS words (
		id UUID primary key,
		word text,
		definition text) """)
    return render_template('index.html')

@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into table
def handle_words():

    new_word = session.prepare("""
    INSERT INTO words(id, word, definition)
    VALUES (?, ?, ?)""")

    session.execute(new_word, [uuid.uuid4(), request.form['word'], request.form['definition']])
    return "ECHO: PUT\n"

@app.route('/words', methods=['GET'])
# query for all the words in the table, returns as json for display on the page.
def display_find():
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
