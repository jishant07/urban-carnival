from main import create_app
from flask_pymongo import PyMongo
from elasticsearch import Elasticsearch

main_app = create_app()

MONGO = PyMongo(main_app).db

ELASTICSEARCH = Elasticsearch("http://localhost:9200")