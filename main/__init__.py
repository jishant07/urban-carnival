from flask import *

def create_app():
    app = Flask(__name__,static_folder="static")
    app.config["MONGO_URI"] = "mongodb://localhost:27017/bigdata"
    return app