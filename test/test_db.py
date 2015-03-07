from dressme import db, User, Outfit, Rating
from flask.ext.sqlalchemy import SQLAlchemy

db.drop_all()
db.create_all()

u = User("matt")
print u

db.session.add(u)
db.session.commit()

print db.session.query(User).all()

u.add_outfit("asdf")

db.session.add(u)
db.session.commit()

print db.session.query(User).all()

matt = db.session.query(User).get("matt")
print matt
