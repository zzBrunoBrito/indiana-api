import os
from flask import Flask
from flask_restful import Resource, reqparse, Api
from flask_sqlalchemy import SQLAlchemy

from services.dezzer_service import DeezerService

app = Flask(__name__)
app.config.from_object('settings.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

from models import user, address, group, list_group, allowed_artist, event, event_list_group


@app.route('/')
def hello():
    return "Hello World!"


class UserResource(Resource):
    def get(self, id):
        user_db = db.session.query(user.User).filter_by(id=id).first()
        if not user_db:
            return {'message': 'Not Found'}, 404
        return {user_db.id: {'name': user_db.name, 'email': user_db.email,
                             'cellphone': user_db.cellphone, 'address': user_db.address.street}}, 201

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('name')
        parser.add_argument('email')
        #parser.add_argument('role')
        parser.add_argument('cellphone')
        parser.add_argument('street')
        parser.add_argument('neighborhood')
        parser.add_argument('number')
        parser.add_argument('city')
        parser.add_argument('state')
        args = parser.parse_args()

        new_user = user.User(username=args['username'], name=args['name'], email=args['email'],
                             cellphone=args['cellphone'])
        new_address = address.Address(street=args['street'], neighborhood=args['neighborhood'],
                                      number=args['number'], city=args['city'], state=args['state'], user=new_user)


        db.session.add(new_user)
        db.session.commit()

        return {new_user.id: {'name': new_user.name, 'email': new_user.email}}, 201

    def put(self, id):
        user_db = db.session.query(user.User).filter_by(id=id).first()

        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('name')
        parser.add_argument('email')
        # parser.add_argument('role')
        parser.add_argument('cellphone')
        args = parser.parse_args()

        user_db.username = args['username']
        user_db.name = args['name']
        user_db.email = args['email']
        user_db.cellphone = args['cellphone']

        db.session.commit()

        return {user_db.id: {'name': user_db.name, 'email': user_db.email}}


class GroupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('street')
        parser.add_argument('neighborhood')
        parser.add_argument('number')
        parser.add_argument('city')
        parser.add_argument('state')
        args = parser.parse_args()

        new_group = group.Group(name=args['name'], owner_id=1)
        new_address = address.Address(street=args['street'], neighborhood=args['neighborhood'],
                                      number=args['number'], city=args['city'], state=args['state'], group=new_group)

        db.session.add(new_address)
        db.session.commit()

        return {new_group.id: {'name:': new_group.name, 'street': new_group.address.street}}


class ListGroupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('allowed_artist_name', action='append')
        args = parser.parse_args()

        new_allowed_artists = [allowed_artist.AllowedArtist(name=name, list_group_id=1) for name in args['allowed_artist_name']]

        new_list_group = list_group.ListGroup(name=args['name'], group_id=1, allowed_artist=new_allowed_artists)

        db.session.add(new_list_group)
        db.session.commit()

        return {'name': new_list_group.name}, 201

    def get(self, id):
        list_group_db = db.session.query(list_group.ListGroup).filter_by(id=id).first()
        if not list_group_db:
            return {'message': 'Not Found'}, 404
        return {list_group_db.id: {'name': list_group_db.name, 'allowed_artists': list_group_db.allowed_artist[0]}}, 201


class AllowedArtistResource(Resource):
    def get(self, list_id):
        parser = reqparse.RequestParser()
        parser.add_argument('query')
        args = parser.parse_args()
        querie = args['query']

        list_group_db = db.session.query(list_group.ListGroup).filter_by(id=list_id).first()
        allowed_artists_db = list_group_db.allowed_artist

        if querie:
            track_list = DeezerService.search_list(querie)
            filtered_list = DeezerService.verify_artist(track_list, allowed_artists_db)
            return filtered_list
        else:
            return allowed_artists_db


class DeezerResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query')
        args = parser.parse_args()
        querie = args['query']
        artists_list = DeezerService.search_artist(querie)
        return artists_list


api.add_resource(UserResource, '/users', endpoint='users', methods=['POST'])
api.add_resource(UserResource, '/users/<int:id>', endpoint='user', methods=['GET', 'PUT'])
api.add_resource(GroupResource, '/groups', endpoint='groups', methods=['POST'])
api.add_resource(ListGroupResource, '/list-groups', endpoint='list-groups', methods=['POST'])
api.add_resource(ListGroupResource, '/list-groups/<int:id>', endpoint='list-group', methods=['GET'])
api.add_resource(AllowedArtistResource, '/list-groups/<int:list_id>/allowed-artists', endpoint='allowed-artist', methods=['GET'])
api.add_resource(DeezerResource, '/deezer/artists', endpoint='deezer-artists', methods=['GET'])

if __name__ == '__main__':
    app.run()
