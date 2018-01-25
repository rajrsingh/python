"""Rabbitmq example for Compose RabbitMQ/Python Grand Tour"""

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

# establishes a connection
channel = connection.channel()

# creates an exchange to deliver messages to
channel.exchange_declare(exchange='grand_tour',
                         exchange_type='direct',
                         durable=True)

# creates the message queue to consume the messages from the exchange
channel.queue_declare(queue='words')

# attaches the queue to the exchange and says any messages with
# a particular routing key should end up in this queue
channel.queue_bind(exchange='grand_tour',
                   queue='words',
                   routing_key='python-msg')

@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')


@app.route('/message', methods=['PUT'])
# Triggers on hitting the 'send' button; sends a message to the queue
def send_message():
    # makes a message from the field in the page
    msg = request.form['message']
    # pushes the message into the exchange
    channel.basic_publish(
        exchange='grand_tour',
        routing_key='python-msg',
        body=msg)
    return msg


@app.route('/message', methods=['GET'])
# Triggers on hitting the 'receive' button; retrieves a message from the queue
def receive_message():
    # retrieves a message from the queue, stores its parts
    method_frame, props, body = channel.basic_get(queue='words', no_ack=True)
    # returns message body or 'no message' for display on page
    if method_frame:
        return body
    else:
        return "{--No Messages in Queue--}"


if __name__ == "__main__":
    app.run()
