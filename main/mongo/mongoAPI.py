from flask import Blueprint
from ..database_init import MONGO

mongoAPI = Blueprint("mongo", __name__)
db = MONGO

@mongoAPI.route("/test")
def new_route():
    try :
        db.users.insert_one({"name": "Jishant"})
        return "Success!"
    except Exception as e:
        return str(e)