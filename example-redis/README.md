## Connecting to Redis from a Python Flask App

#### Package Dependencies
* os
* urllib
* json  
* flask
* redis

#### Connection String
The connection string provided by your Compose Redis deployment should go into an environment variable `COMPOSE_REDIS_URL`.

#### Running the Application
To run the app from the command-line, set and environment variable `FLASK_APP=redis-example.py`, and use the `flask run` command in the same directory as the python file.

