from flask import Blueprint, jsonify
from ..database_init import ELASTICSEARCH
from elasticsearch import helpers
from ..functions import getNDJson
import time
import string
import random

elasticAPI = Blueprint("elastic", __name__)

es_client = ELASTICSEARCH

@elasticAPI.route("/insert/<count>")
def main(count):
    try:
        time_start = time.time()
        response = helpers.bulk(client=ELASTICSEARCH, actions=getNDJson(int(count)),refresh='wait_for')
        time_end = time.time()
        return jsonify({
            "status" : "success",
            "message" : "Documents Inserted Successfully",
            "result" :{
                "time_taken" : round(time_start - time_end),
                "documents_added" : response[0]
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })
    
@elasticAPI.route("/find/<count>")
def find_document(count):
    try:
        time_start = time.time()
        result = es_client.search(index="data",size=int(count),query={"match_all": {}})
        time_end = time.time()
        
        return jsonify({
            "status" : "success", 
            "message" : "Data fetched successfully",
            "result" : {
                "time_taken" : round(time_end - time_start, 2),
                "documents_read" : len(result['hits']['hits']),
                "data_read" : result['hits']['hits']
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })


@elasticAPI.route("/wildcard_search/<value>")
def wildcard_search(value):
    try:
        time_start = time.time()
        temp = '*{}*'.format(value)
        result = es_client.search(index="data",size=10000,query={"wildcard" : {"Item Type.keyword" : {"value" : temp}}})
        time_end = time.time()

        return jsonify({
            "status" : "success",
            "message" : "Search Done Successfully",
            "result" : {
                "time_taken" : round(time_end - time_start, 2),
                "documents_read" : len(result['hits']['hits']),
                "data_read" : result['hits']['hits']
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })
    
@elasticAPI.route("/update/<count>")
def update_query(count):
    try:
        count = int(count)
        random_name = ""
        for i in range(10):
            random_name = random_name + string.ascii_lowercase[random.randint(0, len(string.ascii_lowercase)-10)]

        time_start = time.time()
        result = es_client.search(index="data", size=count, query={"match_all" : {}})
        id_list = []
        for doc in result['hits']['hits']:
            id_list.append(doc['_id'])
        for id in id_list:
            es_client.update(index="data", id = id, body={"doc" : {"Order Priority" : random_name}})
        time_end = time.time()
        return jsonify({
            "staus" : "success",
            "message" : "Update done successfully",
            "result" :{
                "time_taken" : round(time_end - time_start,2),
                "documents_updated" : len(id_list)
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
         })