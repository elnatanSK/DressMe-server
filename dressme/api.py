from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.LargeBinary, unique=False)
    ratings = db.relationship('Rating', backref='outfit', lazy='dynamic')

    def __init__(self, img, ratings=[]):
        self.image = img
        self.ratings = map(Rating,ratings)

    def __repr__(self):
        return '<Outfit %f: %r>' % (self.id, [c.score for c in self.ratings])

class Rating(db.Model):
    score = db.Column(db.Integer, unique=False)
    comment = db.Column(db.String(1024), unique=False)

    def __init__(self, score, comment=''):
        self.score = score
        self.comment = comment

    def __repr__(self):
        return '<rating: %r, "%r">' % (self.score, self.comment)
