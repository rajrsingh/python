import os
from urllib.parse import urlparse
import json

from flask import Flask
from flask import render_template
from flask import request

import mysql.connector


app = Flask(__name__)

# connection string and initialization - sets cursor class to handle python dicts
compose_mysql_url = os.environ['COMPOSE_MYSQL_URL']
path_to_mysql_cert = os.environ['PATH_TO_MYSQL_CERT']
parsed = urlparse(compose_mysql_url)

conn = mysql.connector.connect(
    host=parsed.hostname,
    port=parsed.port,
    user=parsed.username,
    password=parsed.password,
    ssl_ca=path_to_mysql_cert,
    database='grand_tour')


@app.route('/')
# top-level page display, creates table on first run
def serve_page():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS words (
		id serial primary key,
		word varchar(256) NOT NULL,
		definition varchar(256) NOT NULL) """)
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into 'words' table
def handle_words():
    cur = conn.cursor()
    cur.execute("""INSERT INTO words (word, definition)
        VALUES (%s, %s)""", (request.form['word'], request.form['definition']))
    conn.commit()
    return ('', 204)


@app.route('/words', methods=['GET'])
# query for all the words in the table, returns as json for display on the page.
def display_find():
    cur = conn.cursor()
    
    # SQL query for all the rows in the table, stores rows in an object
    cur.execute("""SELECT word, definition FROM words""")
    cursor_obj = cur.fetchall()

    # grabs column names from the table
    labels = [column[0] for column in cur.description]
    
    # makes a list from the dict of the zip of column names and the results object
    results_list = []
    for row in cursor_obj:
        results_list.append(dict(zip(labels, row)))
    
    # makes json from the list for display on the page
    return json.dumps(results_list)


if __name__ == "__main__":
    app.run()
