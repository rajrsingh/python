## Connecting to Compose for MySQL from a Python Flask App

#### Package Dependencies
* os
* urllib
* json  
* flask
* pymysql

#### Connection String
The connection string provided by your Compose Redis deployment should go into an environment variable `COMPOSE_MYSQL_URL`.

#### Running the Application
To run the app from the command-line, set and environment variable `FLASK_APP=mysql-example.py`, and use the `flask run` command in the same directory as the python file.