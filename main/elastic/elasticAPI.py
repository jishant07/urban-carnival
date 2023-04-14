from flask import Blueprint, jsonify
from ..database_init import ELASTICSEARCH
from elasticsearch import helpers
from ..functions import getNDJson
import time

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


@elasticAPI.route("/groupby_country")
def groupby_country():
    return 