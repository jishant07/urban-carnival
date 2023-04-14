from main import create_app
from flask_pymongo import PyMongo
from elasticsearch import Elasticsearch

main_app = create_app()

ELASTICSEARCH = Elasticsearch("http://localhost:9200")

MONGO = PyMongo(main_app).db

# # MONGO.drop_collection("test")
# try:
#     MONGO.create_collection("test")
# except Exception as e:
#     print(str(e))
