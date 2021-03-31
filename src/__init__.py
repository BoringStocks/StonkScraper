from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__, static_folder="")
CORS(app)

from src import viewsV2  # nopep8
