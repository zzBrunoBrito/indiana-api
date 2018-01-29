from app import db


class ListGroup(db.Model):
    __tablename__= 'list_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.CHAR(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    allowed_artist = db.relationship('AllowedArtist', backref='list_group', uselist=True, lazy=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, name, group_id, allowed_artist=None):
        self.name = name
        self.group_id = group_id
        self.allowed_artist = allowed_artist
