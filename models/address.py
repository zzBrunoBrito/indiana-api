from app import db


class Address(db.Model):
    __tablename__= 'address'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.CHAR(100))
    neighborhood = db.Column(db.CHAR(100))
    number = db.Column(db.CHAR(20))
    city = db.Column(db.CHAR(100))
    state = db.Column(db.CHAR(100))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='address', uselist=False, lazy=False)
    group = db.relationship('Group', backref='address', uselist=False, lazy=False)

    def __init__(self, street, neighborhood, number, city, state, user=None, group=None):
        self.street = street
        self.neighborhood= neighborhood
        self.number = number
        self.city = city
        self.state = state
        self.user = user
        self.group = group
