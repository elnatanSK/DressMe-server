from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Text , primary_key = True)
    outfits = db.relationship('Outfit', backref="user_id")

    def __init__(self, uid, outfits=[]):
        self.user_id = uid
        self.outfits = map(Outfit, outfits)

    def add_outfit(self, outfit_image):
        self.outfits.append(Outfit(outfit_image))

    def __repr__(self):
        return '<User %r: %r>' % (self.user_id, [o for o in self.outfits])


class Outfit(db.Model):
    __tablename__ = 'outfits'

    ownder_id = db.Column(db.Text, db.ForeignKey('users.user_id'),
        primary_key = False)
    outfit_id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.LargeBinary, unique=False)
    ratings = db.relationship('Rating', backref="outfit_id")

    def __init__(self, img, ratings=[]):
        self.image = img
        self.ratings = map(Rating, ratings)

    def add_rating(self, rating, comment):
        self.ratings.append(Rating(rating, comment))

    def __repr__(self):
        return '<Outfit owner = %r, id = %r, %r: %r>' % (self.ownder_id,
                self.outfit_id, self.image, self.ratings)


class Rating(db.Model):
    __tablename__ = 'ratings'

    parent_id = db.Column(db.Integer, db.ForeignKey('outfits.outfit_id'),
            primary_key=True)

    score = db.Column(db.Integer, unique=False)
    comment = db.Column(db.Text, unique=False)

    def __init__(self, score, comment=''):
        self.score = score
        self.comment = comment

    def __repr__(self):
        return '<rating: %r, %r>' % (self.score, self.comment)


if __name__ == '__main__':
    db.init_app(app)
