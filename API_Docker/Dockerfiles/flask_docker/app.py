from flask import Flask
import os
import configparser


# flask_token = os.environ['FLASK_TOKEN']
flask_token = 'XXXX'
app = Flask(__name__)

dir_name = "config"
file_name = "flask.ini"
sector = "FLASK"
var = "FLASK_TOKEN2"

def get_from_ini():
    try:
        conf = configparser.ConfigParser()
        # FILE_DIR = os.path.dirname(os.path.dirname(__file__))
        FILE_DIR = os.path.dirname(__file__)
        CONF_FILE_PATH = os.path.join(FILE_DIR, dir_name, file_name)
        conf.read(CONF_FILE_PATH)
        return conf[sector][var]
    except Exception as e:
        return e



@app.route('/')
def hello_world():
    return f'Hello, Docker! token is: {flask_token} ini file {get_from_ini()}'
