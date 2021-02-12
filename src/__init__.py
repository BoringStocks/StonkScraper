from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder="")
CORS(app)

from src import views  # nopep8
