from dressme import db, User, Outfit, Rating
from flask.ext.sqlalchemy import SQLAlchemy

db.drop_all()
db.create_all()

u = User("matt")

db.session.add(u)
db.session.commit()

o = Outfit("<image>")

u.add_outfit(o)
print u

r = Rating(o)
o.add_rating(r)

print "\njson:"
print r
print r.to_dict()
print
print o
print o.to_dict()
print
print
print u
print u.to_dict()
print


db.session.add(u)
db.session.add(o)
db.session.add(r)
db.session.commit()

print db.session.query(Outfit).all()
print db.session.query(User).all()
print db.session.query(Rating).all()

print
print

u2 = User("Zach")

u2.assign_rating(r)
db.session.add(r)
db.session.add(u2)
db.session.commit()


print db.session.query(Outfit).all()
print db.session.query(User).all()
print db.session.query(Rating).all()

print db.session.query(User).get("matt")
print db.session.query(User).get("taylor")

#print db.session.query(User).all()
#
#u.add_outfit("asdf")
#
#db.session.add(u)
#db.session.commit()
#
#print db.session.query(User).all()
#
#matt = db.session.query(User).get("matt")
#print matt
#
#o = matt.outfits[0]
#print o
#o.add_rating(4, "not too bad at all")
#print o
#
#db.session.add(o)
#db.session.commit()
#print db.session.query(User).all()
#
#u2 = User("zach")
#u2.add_outfit("<zachs outfit pic>")
#db.session.add(u2)
#db.session.commit()
#print db.session.query(User).all()
#
