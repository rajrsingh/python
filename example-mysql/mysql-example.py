import os
from urllib.parse import urlparse
import json

from flask import Flask
from flask import render_template
from flask import request

import pymysql.cursors


app = Flask(__name__)

# connection string and initialization
compose_mysql_url = os.environ['COMPOSE_MYSQL_URL']
parsed = urlparse(compose_mysql_url)

conn = pymysql.connect(
    host=parsed.hostname,
    port=parsed.port,
    user=parsed.username,
    password=parsed.password,
    db='grand_tour',
    cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
# top-level page display
def serve_page():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS words (
		id serial primary key,
		word varchar(256) NOT NULL,
		definition varchar(256) NOT NULL) """)
    return render_template('index.html')


@app.route('/words', methods=['PUT'])
# triggers on hitting the 'Add' button; inserts word/definition into collection
def handle_words():
    cur = conn.cursor()
    cur.execute("""INSERT INTO words (word, definition)
        VALUES (%s, %s)""", (request.form['word'], request.form['definition']))
    conn.commit()
    return "ECHO: PUT\n"


@app.route('/words', methods=['GET'])
# query for all the words in the collection, returns as json for display on the page.
def display_find():
    cur = conn.cursor()
    cur.execute("""SELECT word, definition FROM words""")
    results_list = cur.fetchall()

    return json.dumps(results_list)


if __name__ == "__main__":
    app.run()
