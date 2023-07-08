# application.py

from flask import Flask
import os
from flask_executor import Executor

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
ALLOWED_EXTENSIONS = {'txt'}
executor = Executor()  # make executor a global variable

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    executor.init_app(app)  # initialize the global executor with your app
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app
