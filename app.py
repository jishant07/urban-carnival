from main import create_app


app = create_app()

from main.mongo.mongoAPI import mongoAPI
from main.elastic.elasticAPI import elasticAPI

app.register_blueprint(mongoAPI, url_prefix="/mongo")
app.register_blueprint(elasticAPI, url_prefix="/elastic")

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)