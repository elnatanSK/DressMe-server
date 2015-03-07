from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.LargeBinary, unique=False)

    def __init__(self, img, ratings=[]):
        self.image = img
        self.ratings = map(Rating,ratings)

    def __repr__(self):
        return '<Outfit %f: %r>' % (self.id, [c.score for c in self.ratings])

if __name__ == '__main__':
    db.init_app(app)

