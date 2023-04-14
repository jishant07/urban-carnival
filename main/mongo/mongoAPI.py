from flask import Blueprint
from ..database_init import MONGO

mongoAPI = Blueprint("mongo", __name__)

@mongoAPI.route("/test")
def new_route():
    print(MONGO)
    return "FROM THE NEW ROUTE"