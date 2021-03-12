from flask_restful import Api
from . import app
from .services.UserService import UserService
from .services.DataService import DataService

api = Api(app)

#Définition des end-points pour les classes de models.py
api.add_resource(UserService, '/users','/users/<int:id>', '/users/<string:all>', '/users/<int:id>/<string:column>', '/users/<string:column>/<string:regex>')
api.add_resource(DataService, '/data', '/data/<int:id>', '/data/<int:id>/<string:column>', '/data/<string:column>/<string:regex>')

