from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
import collections
from datetime import date
from ..models import Data

"""Ensemble des requêtes possibles via l'url ip/users"""
class DataService(Resource):
    #Vérifie si le 
    decorators = [jwt_required()]
    """Renvoie les donnée de la ligne spécifiée, les donnée de la ligne et de la colonne spécifiée ou de la colonne et de la regex spécifiée"""
    def get(self, id=None, regex=None, column=None):
        
        if regex != None and column != None:
            if column not in Data.get_column() :
                return {"error" : "Wrong field name in url"}
            
            data = Data.query.filter(getattr(Data, column).op('SIMILAR TO')(f'{regex}')).all()
           
            if data == [] :
                return {"error" : "Nothing found"}, 400
  
            return [d.to_dict() for d in data]
        
        if id == None:
            return {"error": "Location id not specified"}, 400

        data = Data.query.get(id)
        
        if data == None:
            return {"error": "Location not found"}, 404
        
        data_dict = data.to_dict()
         
        if column == None :
            return data_dict
        elif column in data_dict.keys() :
            return {f"{column}" : data_dict[column]}
        else:
            return  {"error" : "Field does not exist"}, 404
            
    """Met à jour les données d'une localisation via une requête contenant un body au format json, les champs de la tables sont matchs automatiquement pour ne pas avoir à tout repréciser. Renvoie une erreur si la colonne spécifiée dans le body n'existe pas."""
    def post(self, id=None):
        if id == None:
            return {"error": "Location id not specified"}, 400
        
        #If no body
        if(request.json == None ):
            return {"error": "Nothing in body"}, 400
        
        data = Data.query.get(id)
        
        if data == None :
            return {"error": "Location not found"}, 404  
        
        if Data.update_data(data, request.json):
            return {"status": "ok"}
        else:
            return {"error": "Wrong fields"}, 400
        
    """Ajoute une localisation dans la base de donnée d'après un body au format json envoyé dans la requête. Le body doit contenir toutes les colonnes de la table sinon renvoie une erreur."""
    def put(self):
        #If no body
        if(request.json == None ):
            return {"error": "Nothing in body"}, 400
        
        #If wrong field in body
        if not collections.Counter(request.json.keys()) == collections.Counter(Data.get_column()):
            return {"error": "Wrong fields"}, 400
    
        Data.add_data(Data(
            request.json['geonameid'],
            request.json['name'],
            request.json['asciiname'],
            request.json['alternate_names'],
            request.json['latitude'],
            request.json['longitude'],
            request.json['feature_class'],
            request.json['feature_code'],
            request.json['country_code'],
            request.json['cc2'],
            request.json['admin1'],
            request.json['admin2'],
            request.json['admin3'],
            request.json['admin4'],
            request.json['population'],
            request.json['elevation'],
            request.json['dem'],
            request.json['timezone'],
            date.today()
        ))
        return {'status': 'ok'}
        
    """Supprime une localisation de la table si l'id spécifiée dans l'url existe."""
    def delete(self, id=None):
        if(id == None):
            return {"error": "Location id not specified"}, 400
        
        data = Data.query.get(id)
    
        
        if(data== None):
            return {"error": "Location not found"}, 404
        
        Data.remove_data(data)
        
        return {"status": "ok"}
        
