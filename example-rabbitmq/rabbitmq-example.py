import os
from urllib.parse import urlparse

from flask import Flask
from flask import render_template
from flask import request

import pika

app = Flask(__name__)

# connection string and initialization
compose_rabbitmq_url = os.environ['COMPOSE_RABBITMQ_URL']
parsed = urlparse(compose_rabbitmq_url)

credentials = pika.PlainCredentials(parsed.username, parsed.password)
vhost = parsed.path.replace("/","")

parameters = pika.ConnectionParameters(
    host=parsed.hostname,
    port=parsed.port,
    credentials=credentials,
    virtual_host=vhost,
    ssl=True
)

connection = pika.BlockingConnection(parameters)


@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')


@app.route('/message', methods=['PUT'])
# triggers on hitting the 'send' button; sends a message to the queue
def send_message():
    # makes a message from the field in the page
    msg = request.form['message']
    # establishes a connection
    channel = connection.channel()
    # selects or creates the message queue
    channel.queue_declare(queue='grand_tour')
    # pushes the message onto the queue
    channel.basic_publish(
        exchange='',
        routing_key='grand_tour',
        body=msg)
    return msg


@app.route('/message', methods=['GET'])
# triggers on hitting the 'receive' button; retrieves a message from the queue
def receive_message():
    # establishes a connection
    channel = connection.channel()
    # selects or creates the message queue
    channel.queue_declare(queue='grand_tour')
    # retrieves a message from the queue, stores its parts
    method_frame, properties, body = channel.basic_get(queue = 'grand_tour', no_ack=True)
    # returns message body or 'no message' for display on page
    if method_frame == None:
        return "{--No Messages in Queue--}"
    else:
        return body


if __name__ == "__main__":
    app.run()
