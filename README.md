# The Grand Tour - Python
A set of example applications that will add word/definition pairs to a database running on Compose.

This repo contains the apps written in Python 3.6.0 and uses Flask. It is intended to run locally, for example and experimentation purposes only.

## Running the Example
To run, cd into the <_db_>-example directory, export your Compose connection string as an environment variable, set the flask app variable:
`export FLASK_APP=<_db_>-example.py`
and then:
`flask run`

The application will be served on 127.0.0.1:5000 and can be opened in a browser.
