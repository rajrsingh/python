## Connecting to Scylla from a Python Flask App

#### Package Dependencies
* os
* ssl
* urllib
* uuid
* json
* flask
* cassandra

#### Connection String and Certificate
The connection string provided by your Compose RethinkDB deployment should go into an environment variable `COMPOSE_SCYLLA_URL`.
Download a copy of the certificate and put it's path in an environment variable `PATH_TO_SCYLLA_CERT`

#### Running the Application
To run the app from the command-line, set and environment variable `FLASK_APP=scylla-example.py`, and use the `flask run` command in the same directory as the python file.