import os
from urllib.parse import urlparse
import json

from flask import Flask
from flask import render_template
from flask import request

import psycopg2


app = Flask(__name__)

# connection string and db connection initialization
compose_postgresql_url = os.environ['COMPOSE_POSTGRESQL_URL']
path_to_postgresql_cert = os.environ['PATH_TO_POSTGRESQL_CERT']
parsed = urlparse(compose_postgresql_url)
conn = psycopg2.connect(
    host=parsed.hostname,
    port=parsed.port,
    user=parsed.username,
    password=parsed.password,
    sslmode='verify-ca',
    sslrootcert=path_to_postgresql_cert,
    database='grand_tour')


@app.route('/')
# top-level page display, creates table if it doesn't exist
def serve_page():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS words (
		id serial primary key,
		word varchar(256) NOT NULL,
		definition varchar(256) NOT NULL) """)
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into table
def handle_words():
    cur = conn.cursor()
    cur.execute("""INSERT INTO words (word, definition)
        VALUES (%s, %s)""", (request.form['word'], request.form['definition']))
    conn.commit()
    return "ECHO: PUT\n"


@app.route('/words', methods=['GET'])
# query for all the rows in the table,\
# makes a dictionary object from the column names and the results,\
# makes json from the dict for display on the page.
def display_find():
    cur = conn.cursor()
    cur.execute("""SELECT word, definition FROM words""")
    cursor_obj = cur.fetchall()

    labels = [column[0] for column in cur.description]
    results_list = []

    for row in cursor_obj:
        results_list.append(dict(zip(labels, row)))

    return json.dumps(results_list)

if __name__ == "__main__":
    app.run()
