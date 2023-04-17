from flask import *
from ..database_init import MONGO
from ..functions import getRandomData
from pymongo import UpdateOne
import time
import random
import string

mongoAPI = Blueprint("mongo", __name__)
db = MONGO

def cursor_to_data(cursor):
    data = []
    for doc in cursor:
        data.append(doc)
    return data

@mongoAPI.route("/insert/<count>")
def getting_data(count):
    data_to_write = getRandomData(count)
    try:
        time_start = time.time()
        temp = db.data.insert_many(data_to_write)
        time_end = time.time()
        return jsonify({
            "status" : "success",
            "message" : "Data Inserted Successfully",
            "result" : {
                "documents_inserted" : len(temp.inserted_ids),
                "time_taken" : round(time_end - time_start,2)
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })

@mongoAPI.route("/find/<count>")
def getCountData(count):
    count = int(count)
    if count == 0:
        count = 100
    try:
        time_start = time.time()
        result = db.data.find({},{"_id": 0}).limit(count)
        time_end = time.time()
        
        data = cursor_to_data(result)

        return jsonify({
            "status" : "success", 
            "message" : "Fetch Successful",
            "result" : {
                "time_taken" : round(time_end - time_start, 2),
                "documents_read" : len(data),
                "data_read" : data
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })

@mongoAPI.route("/country_groupby")
def aggregate():
    time_start = time.time()
    filter_data = db.data.aggregate([{"$group" : {"_id" : "$Country", "count" : {'$sum' : 1}}}])
    time_end =  time.time()
    
    data = cursor_to_data(filter_data)
    
    return jsonify({
        "status" : "success", 
        "message" : "Group by query run successfully",
        "result" : {
            "time_taken" : round(time_end - time_start,2),
            "documents_read" : len(data),
            "data_read" : data 
        }
    })


@mongoAPI.route("/wildcard_search/<value>")
def wildcard(value):
    time_start = time.time()
    wildcard_data = db.data.find({'Item Type': {'$regex': '.*{}.*'.format(value)}},{"_id" : 0}).limit(10000)
    time_end = time.time()

    data = cursor_to_data(wildcard_data)

    return jsonify({
        "status" : "success",
        "message" : "Wildcard Search Done Successfully",
        "result" : {
            "time_taken" : round(time_end - time_start, 2),
            "documents_read" : len(data),
            "data_read" : data  
        }
    })

@mongoAPI.route("/update/<count>")
def data_update(count):
    random_name = ""
    for i in range(10):
        random_name = random_name + string.ascii_lowercase[random.randint(0, len(string.ascii_lowercase)-10)]
    
    try:
        bulk_request = []
        time_start = time.time()
        for doc in db.data.find({}).limit(int(count)):
            bulk_request.append(UpdateOne({'_id' : doc["_id"]}, {'$set' : {"Order Priority" : random_name}},True))
        result = db.data.bulk_write(bulk_request)
        time_end = time.time()

        return jsonify({
            "status" : "success",
            "message" : "Update done successfully",
            "result" : {
                "time_taken" : round(time_end -  time_start),
                "documents_changed" : result.modified_count
            }
        })
    except Exception as e:
        return jsonify({
            "status" : "failure",
            "message" : str(e)
        })