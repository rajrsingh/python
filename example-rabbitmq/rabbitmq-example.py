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
    msg = request.form['message']

    channel = connection.channel()
    channel.queue_declare(queue='grand_tour')
    channel.basic_publish(
        exchange='',
        routing_key='grand_tour',
        body=msg)

    return msg


@app.route('/message', methods=['GET'])
# triggers on hitting the 'receive' button; retrieves a message to the queue
def receive_message():
    channel = connection.channel()
    channel.queue_declare(queue='grand_tour')

    method_frame, properties, body = channel.basic_get(queue = 'grand_tour', no_ack=True)
    if method_frame == None:
        return "{--No Messages in Queue--}"
    else:
        return body


if __name__ == "__main__":
    app.run()
