from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
import collections
from collections import OrderedDict
from datetime import date
from ..models import Users

"""Ensemble des requêtes possibles via l'url ip/data"""
class UserService(Resource):
    decorators = [jwt_required()]

    """Renvoie les donnée de la ligne spécifiée, les donnée de la ligne et de la colonne spécifiée ou de la colonne et de la regex spécifiée"""
    def get(self, id=None, all=None, column=None, regex=None):
        if regex != None and column != None:
            if column not in Users.get_column() :
                return {"error" : "Wrong field name in url"}
            
            users = Users.query.filter(getattr(Users, column).op('SIMILAR TO')(f'{regex}')).all()
           
            if users == [] :
                return {"error" : "Nothing found"}, 400
  
            return [OrderedDict((k, d.to_dict().get(k)) for k in ["id"] + Users.get_column() + ["mise_a_jour"]) for d in users]
        
        if(all == "all"):
            return [OrderedDict((k, user.to_dict().get(k)) for k in ["id"] + Users.get_column() + ["mise_a_jour"]) for user in Users.query.all()]
        elif(id == None):
            return {"error": "User id not specified"}, 400

        user = Users.query.get(id)
        
        if(user == None):
            return {"error": "User not found"}, 404
        
        user_dict = OrderedDict((k, user.to_dict().get(k)) for k in ["id"] + Users.get_column() + ["mise_a_jour"])
         
        if column == None :
            return user_dict
        elif column in user_dict.keys() :
            return {f"{column}" : user_dict[column]}
        else:
            return  {"error" : "Field does not exist"}, 404

    """Met à jour les données d'un utilisateur via une requête contenant un body au format json, les champs de la tables sont matchs automatiquement pour ne pas avoir à tout repréciser. Renvoie une erreur si la colonne spécifiée dans le body n'existe pas."""
    def post(self, id=None):
        if id == None:
            return {"error": "User id not specified"}, 400
        
        #If no body
        if(request.json == None ):
            return {"error": "Nothing in body"}, 400
        
        user = Users.query.get(id)
        
        if user == None :
            return {"error": "User not found"}, 404  
        
        if Users.update_user(user, request.json):
            return {"status": "ok"}
        else:
            return {"error": "Wrong fields"}, 400
        
    """Ajoute un utilisateur dans la base de donnée d'après un body au format json envoyé dans la requête. Le body doit contenir toutes les colonnes de la table sinon renvoie une erreur."""
    def put(self):
        #If no body
        if(request.json == None ):
            return {"error": "Nothing in body"}, 400
        
        #If wrong field in body
        if not collections.Counter(request.json.keys()) == collections.Counter(Users.get_column()):
            return {"error": "Wrong fields"}, 400
    
        Users.add_user(Users(
            request.json['nom'],
            request.json['prenom'],
            request.json['fonction'],
            request.json['anciennete'],
            date.today(),
            request.json['conge'],
            request.json['actif'],
            request.json['actionnaire'],
            request.json['missions']
        ))
        return {'status': 'ok'}
    
    """Supprime un utilisateur de la table si l'id spécifiée dans l'url existe."""
    def delete(self, id=None):
        if(id == None):
            return {"error": "User id not specified"}, 400
        
        user = Users.query.get(id)
    
        
        if(user == None):
            return {"error": "User not found"}, 404
        
        Users.remove_user(user)
        
        return {"status": "ok"}
        
