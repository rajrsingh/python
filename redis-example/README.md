## Connecting to Redis from a Python Flask App

#### Summary
Stores word/definition pairs as keys/values in a hash map named 'words'. The driver defualts to database '0' since none is specified in the connection string. Gets all existing words, creates a JSON object, and returns all words to display on the page.

#### Package Dependencies
* flask
* redis
* urllib
* os
* json

#### Connection String
The connection string provided by your Compose Redis deployment should go into an environment variable `REDIS_URL`.

#### Running the Application
To run the app from the command-line, set and environment variable `FLASK_APP=redis-example.py`, and use the `flask run` command in the same directory as the python file.

