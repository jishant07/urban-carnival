from flask import Blueprint
from ..database_init import ELASTICSEARCH

elasticAPI = Blueprint("elastic", __name__)

@elasticAPI.route("/")
def main():
    print(ELASTICSEARCH)
    return "Works!!"