from flask import Flask

app = Flask(__name__, static_folder="")

from src import views  # nopep8
