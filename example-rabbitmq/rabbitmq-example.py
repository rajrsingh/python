import os
from urllib.parse import urlparse

from flask import Flask
from flask import render_template
from flask import request

import pika

app = Flask(__name__)

# connection string, auth, and connection parameters set
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

# establish a connection, open an ampq channel, specifiy the exchange
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='grand_tour',
    exchange_type='direct',
    durable=True)


@app.route('/')
# top-level page display
def serve_page():
    return render_template('index.html')


@app.route('/message', methods=['PUT'])
# triggers on hitting the 'send' button; sends a message to the queue
def send_message():
    # makes a message from the field in the page
    msg = request.form['message']
    
    # pushes the message onto the queue
    channel.basic_publish(
        exchange='grand_tour',
        routing_key='python-msg',
        body=msg)
    return msg


@app.route('/message', methods=['GET'])
# triggers on hitting the 'receive' button; retrieves a message from the queue
def receive_message():
    # creates the message queue to consume the messages in the exchange
    channel.queue_declare(queue='words')
    
    # tells the queue to pay attenetion to the exchange and messages with the routing key
    channel.queue_bind(exchange='grand_tour',
        queue='words',
        routing_key='python-msg')
    
    # retrieves a message from the queue, stores its parts
    method_frame, properties, body = channel.basic_get(queue = 'words', no_ack=True)
    
    # returns message body or 'no message' for display on page
    if method_frame == None:
        return "{--No Messages in Queue--}"
    else:
        return body


if __name__ == "__main__":
    app.run()
