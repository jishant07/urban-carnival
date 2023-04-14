import csv
import os
from main import create_app
import random

app = create_app()

def getRandomData(count = 10000):
    file = open(os.path.join(app.static_folder,"dummy_data.csv"))
    reader = csv.DictReader(file)        
    index = 0
    data = []
    for row in reader:
        data.append(row)
        index = index + 1
        if index == int(count):
            break
    return data

def getNDJson(count = 1000):
    index = 0
    data = getRandomData(count)
    for doc in data:
        index = ""
        for i in range(10):
            index = index + str(random.randint(0, 9))
        doc = {
                "_index": "data",
                "_id": int(index),
                "_source": {
                    "id": int(index),
                    "Region" : doc["Region"],
                    "Country" : doc["Country"],
                    "Item Type" : doc["Item Type"],
                    "Sales Channel" : doc["Sales Channel"],
                    "Order Priority" : doc["Order Priority"],
                    "Order Date" : doc["Order Date"],
                    "Order ID" : doc["Order ID"],
                    "Ship Date" : doc["Ship Date"],
                    "Units Sold" : doc["Units Sold"],
                    "Unit Price" : doc["Unit Price"],
                    "Unit Cost" : doc["Unit Cost"],
                    "Total Revenue" : doc["Total Revenue"],
                    "Total Cost" : doc["Total Cost"],
                    "Total Profit" : doc["Total Profit"]
                },
            }
        yield doc