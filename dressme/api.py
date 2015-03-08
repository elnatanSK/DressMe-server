from flask import Flask, request, Request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import flask.json as json


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

    def to_dict(self):
        return {'user_id': self.user_id,
                'outfits': map(Outfit.to_dict, self.outfits),
                'rating_queue': map(Rating.to_dict, self.rating_queue)
                }

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

    def to_dict(self):
        own_id = "<NONE>"
        out_id = "<NONE>"
        if self.owner is not None:
            own_id = self.owner.user_id
        if self.outfit_id is not None:
             out_id = self.outfit_id
        return {'owner_id': own_id,
                'outfit_id': out_id,
                'image': self.image,
                'ratings': map(Rating.to_dict, self.ratings)
                }


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
        outfit.add_rating(self)


    def __repr__(self):
        return '<reviewer: %r, outfit: %r,  rating: %r, %r>' % (self.reviewer_id, self.reviewed_outfit, self.score, self.comment)

    def to_dict(self):
        uid = "<NONE>"
        comment = "<NONE>"
        score = 0
        if self.reviewer is not None:
            uid = self.reviewer.user_id
        if self.comment is not None:
            comment = self.comment
        if self.score is not None:
            score = self.score
        return {'reviewer_id': uid,
                'score': score,
                'comment': comment
                }

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

#
# POST {
#
@app.route('/users/<uid>/outfits/', methods = ['GET','POST'])
def do_outfits(uid):
    user = db.session.query(User).get(uid)
    if user is None:
        return "No Such user %r" % uid, 300
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        img = request.json['image']
        o = Outfit(img)
        user.add_outfit(o)
        db.session.add(user)
        db.session.commit()
    return jsonify({'user_id': uid,
                    'outfits': map(Outfit.to_dict, user.outfits)
                    })

@app.route('/users/<uid>/rating_queue/', methods = ['GET'])
def do_rating_queue(uid):
    user = db.session.query(User).get(uid)
    if user is None:
        return "Not such user: %s" % uid, 300
    if request.method == 'GET':
        return jsonify({'reviewer_id': uid,
            'outfits': map(outfit_dict_for_rating, user.rating_queue)
            })

def outfit_dict_for_rating(rating):
    d = rating.outfit_id.to_dict()
    del d['ratings']
    return d


# POST { 'score': <INT>
#      , 'comment': <String>
#      , 'reviewer_id': <String>
#      }
@app.route('/outfits/<oid>/ratings/', methods = ['GET','POST'])
def do_ratings(oid):
    out = db.session.query(Outfit).get(oid)
    if out is None:
        return "No Such outfit: %r" % oid, 300
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        score = request.json['score']
        comment = request.json['comment']
        rev_id = request.json['reviewer_id']
        r = Rating(out)
        r.comment = comment
        r.score = score
        r.reviewer_id = rev_id
        db.session.add(out)
        db.session.add(r)
        db.session.commit()
    return jsonify({'outfit_id': oid,
                    'ratings': map(Rating.to_dict, out.ratings)
                    })





if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
