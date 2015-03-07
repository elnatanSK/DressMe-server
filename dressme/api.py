from flask import Flask, request, Request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Text, primary_key = True)

    outfits = db.relationship('Outfit', backref="owner")

    rating_queue = db.relationship('Rating', backref="reviewer")

    def __init__(self, uid):
        self.user_id = uid
        self.outfits = []
        self.rating_queue = []


    def add_outfit(self, outfit):
        self.outfits.append(outfit)

    def assign_rating(self, rating):
        rating.reviewer_id = self.user_id
        self.rating_queue.append(rating)


    def __repr__(self):
        return '<User %r: %r, rating_queue = %r>' % (self.user_id,
                self.outfits, self.rating_queue)


class Outfit(db.Model):
    __tablename__ = 'outfits'

    owner_id = db.Column(db.Text, db.ForeignKey('users.user_id'),
        primary_key = False)
    outfit_id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.LargeBinary, unique=False)
    ratings = db.relationship('Rating', backref="outfit_id")

    def __init__(self, img, ratings=[]):
        self.image = img
        self.ratings = map(Rating, ratings)

    def add_rating(self, rating):
        self.ratings.append(rating)

    def __repr__(self):
        return '<Outfit owner = %r, id = %r, %r: %r>' % (self.owner_id,
                self.outfit_id, self.image, self.ratings)


class Rating(db.Model):
    __tablename__ = 'ratings'

    reviewer_id = db.Column(db.Text, db.ForeignKey('users.user_id'), unique=False)
    reviewed_outfit = db.Column(db.Text, db.ForeignKey('outfits.outfit_id'))
    rating_id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=False)
    comment = db.Column(db.Text, unique=False)
    assigned = db.Column(db.Boolean)

    def __init__(self, outfit):
        self.assigned = False
        self.reviewed_outfit = outfit


    def __repr__(self):
        return '<reviewer: %r, outfit: %r,  rating: %r, %r>' % (self.reviewer_id, self.reviewed_outfit, self.score, self.comment)

# /users/ is the endpoint to create a user
#
# POST { id: 'facebook user id'}
#
@app.route('/users/', methods=['POST'])
def add_user():
    if request.method == 'POST':
        uid = request.json['id']
        if db.session.query(User).get(uid):
            return "User %s already exits" % uid, 300
        u = User(uid)
        db.session.add(u)
        db.session.commit()
        return "Added %s" % uid, 200

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
