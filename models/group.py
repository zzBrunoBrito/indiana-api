from app import db


class Group(db.Model):
    __tablename__= 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.CHAR(50))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    list_group = db.relationship('ListGroup', backref='group', uselist=True, lazy=False)
    event = db.relationship('Event', backref='group', uselist=True, lazy=False)

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id