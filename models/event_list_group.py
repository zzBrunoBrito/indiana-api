from app import db


class EventListGroup(db.Model):
    __tablename__= 'event_list_group'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    list_group_id = db.Column(db.Integer, db.ForeignKey('list_group.id'))

    event = db.relationship('Event', backref='event_list_group')
    list_group = db.relationship('ListGroup', backref='event_list_group')

    def __init__(self, event_id, list_group_id):
        self.event_id = event_id
        self.list_group_id = list_group_id
