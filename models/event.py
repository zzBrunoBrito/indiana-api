from app import db


class Event(db.Model):
    __tablename__= 'event'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.CHAR(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime())
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    artists_lists = db.relationship('ListGroup', secondary='event_list_group', backref='events', lazy=True)

    def __init__(self, code, group_id, artists_lists):
        self.code = code
        self.group_id = group_id
        self.artists_lists = artists_lists
