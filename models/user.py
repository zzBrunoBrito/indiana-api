import enum

from sqlalchemy.dialects import postgresql

from app import db


class User(db.Model):
    __tablename__= 'user'

    class Roles(enum.Enum):
        ROOT = 'ROOT'
        SUPPORT = 'Suporte'
        ONWER = 'Lider'
        HELPER = 'Ajudante'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.CHAR(30))
    name = db.Column(db.CHAR(100))
    email = db.Column(db.CHAR(50))
    role = db.Column(postgresql.ENUM(Roles, create_type=False))
    cellphone = db.Column(db.CHAR(30))
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    date_joined = db.Column(db.DateTime)
    #address = db.relationship('Address', backref='user', uselist=False, lazy=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    group = db.relationship('Group', backref='user', uselist=False, lazy=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, name, email, cellphone, address_id=None):
        self.username = username
        self.name = name
        self.email = email
        self.cellphone = cellphone
        self.address_id = address_id
    #
    # def __repr__(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'name': self.name,
    #         'email': self.email,
    #         'role': self.role,
    #         'cellphone': self.cellphone
    #     }