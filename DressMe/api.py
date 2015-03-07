from flask import Flask, jsonify
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self, id):
        return "Hello %s!" % id

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(Hello, '/outfits/<string:id>', endpoint = 'user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
