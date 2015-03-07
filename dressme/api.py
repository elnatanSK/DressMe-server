from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy

import dressme

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
api = Api(app)
db = SQLAlchemy(app)
app.db = db

api.add_resource(Hello, '/hello/<string:id>', endpoint = 'user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
