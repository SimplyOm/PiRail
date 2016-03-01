from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    food = db.Column(db.String(20), index=True)
    sanitation = db.Column(db.String(20), index=True)
    journey = db.Column(db.String(20), index=True)
    feedback= db.Column(db.String(200), index=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    seat = db.Column(db.Integer, index=True)
    password=db.Column(db.String(4),index=True)

    def __repr__(self):
        return '<Chart %r>' % (self.name)
