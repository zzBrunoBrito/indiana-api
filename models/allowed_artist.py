from app import db


class AllowedArtist(db.Model):
    __tablename__= 'allowed_artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.CHAR(100), nullable=False)
    list_group_id = db.Column(db.Integer, db.ForeignKey('list_group.id'))
    created_at = db.Column(db.DateTime)

    def __init__(self, name, list_group_id):
        self.name = name
        self.group_id = list_group_id
