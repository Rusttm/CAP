from flask import Flask
import os
flask_token = os.environ['FLASK_TOKEN']


app = Flask(__name__)



@app.route('/')
def hello_world():
    return f'Hello, Docker! token is: {flask_token}'
