from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import date
import csv
import simplejson
from simplejson.compat import StringIO
import logging as lg
from . import app

db = SQLAlchemy(app)

"""Modèle de la table 'users' de la base de données"""
class Users(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    fonction = db.Column(db.String(1000), nullable=False)
    anciennete = db.Column(db.Integer, nullable=False)
    mise_a_jour = db.Column(db.Date, nullable=False)
    conge = db.Column(db.Integer, nullable=False)
    actif = db.Column(db.Boolean, nullable=False)
    actionnaire = db.Column(db.Boolean, nullable=False)
    missions = db.Column(db.ARRAY(db.String))
    
    file = "./Data/users.json"

    def __init__(self, nom, prenom, fonction, anciennete, mise_a_jour, conge, actif, actionnaire, missions):
        self.nom = nom
        self.prenom = prenom
        self.fonction = fonction
        self.anciennete = anciennete
        self.mise_a_jour = mise_a_jour
        self.conge = conge
        self.actif = actif
        self.actionnaire = actionnaire
        self.missions = missions

    """Permet de mettre à jour un utilisateur dans la table users,si le body de la requete put est bien formé et contient au moins 1 colonne de la table."""
    @staticmethod
    def update_user(user, json):
        columns = Users.get_column()
        
        for key, value in json.items():
            if key not in columns :
                return False
            
            setattr(user, key, value)
        db.session.commit()
        return True

    """Permet d'ajouter un utilisateur dans la table users, si le body contient toutes les colonnes de la table."""
    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commit()
        
    """Permet de supprimer un utilisateur dans la table users s'il existe."""
    @staticmethod
    def remove_user(user):
        db.session.delete(user)
        db.session.commit()
      
    """Renvoie une liste du nom des colonnes de la table users..."""
    @staticmethod
    def get_column():
        table = db.metadata.tables["users"]
        return [column.name for column in table.c if column.name != "id" and column.name != "mise_a_jour"]
        
"""Modèle de la table 'data' de la base de données"""
class Data(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    geonameid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    asciiname = db.Column(db.String(200), nullable=False)
    alternate_names = db.Column(db.String(10000), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    feature_class = db.Column(db.String(1), nullable=False)
    feature_code = db.Column(db.String(10), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    cc2 = db.Column(db.String(200), nullable=True)
    admin1 = db.Column(db.String(20), nullable=False)
    admin2 = db.Column(db.String(80), nullable=True)
    admin3 = db.Column(db.String(20), nullable=True)
    admin4 = db.Column(db.String(20), nullable=True)
    population = db.Column(db.Integer, nullable=False)
    elevation = db.Column(db.Integer, nullable=True)
    dem = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.String(40), nullable=False)
    modification_date = db.Column(db.Date, nullable=False)
    
    file = "./Data/FR.tsv"

    def __init__(self, geonameid, name, asciiname, alternate_names, latitude, longitude, feature_class, feature_code, country_code, cc2, admin1, admin2, admin3, admin4, population, elevation, dem, timezone, modification_date):
        self.geonameid = geonameid
        self.name = name
        self.asciiname = asciiname
        self.alternate_names = alternate_names
        self.latitude = latitude
        self.longitude = longitude
        self.feature_class = feature_class
        self.feature_code = feature_code
        self.country_code = country_code
        self.cc2 = cc2
        self.admin1 = admin1
        self.admin2 = admin2
        self.admin3 = admin3
        self.admin4 = admin4
        self.population = population
        self.elevation = elevation
        self.dem = dem
        self.timezone = timezone
        self.modification_date = modification_date
        
    """Permet d'ajouter une localisation dans la table data, si le body contient au moins une colonne de la table."""
    @staticmethod
    def update_data(data, json):
        columns = Data.get_column()
        
        for key, value in json.items():
            if key not in columns :
                return False
            
            setattr(data, key, value)
        db.session.commit()
        return True

    """Permet d'ajouter une localisation dans la table data, si le body contient toutes les colonnes de la table."""
    @staticmethod
    def add_data(data):
        db.session.add(data)
        db.session.commit()
        
    """Permet de supprimer une localisation dans la table data si elle existe"""
    @staticmethod
    def remove_data(data):
        db.session.delete(data)
        db.session.commit()
        
    """Renvoie une liste du nom des colonnes de la table users..."""    
    @staticmethod
    def get_column():
        table = db.metadata.tables["data"]
        return [column.name for column in table.c if column.name != "id" and column.name != "modification_date"]

"""Remplit la base de données avec les lignes des variables de la classe si les tables n'existent pas dans la base de donnée."""
def init_db():
    
    if not db.get_engine().has_table("users") or not db.get_engine().has_table("data"):
        
        db.create_all()
       
        # Import dans la base de données table users depuis le fichier users.json
        with open(Users.file, 'r') as file :
            jsonfile = file.read()
            io = StringIO(jsonfile)
            obj = simplejson.load(io)
            for item in obj:
                data = obj[item]
                db.session.add(Users(data['nom'], data['prenom'], data['fonction'],
                                    data['anciennete'], date.today(), data['conge'], data['actif'], data['actionnaire'], data['missions']))
                
        
        db.session.commit()      
        #Import dans la base de données table data depuis le fichier FR.tsv
        with open(Data.file, newline ='', errors='ignore') as file :
            reader = csv.reader(file, delimiter='\t', quotechar='"') 
            for row in reader :
                if row[15] == "":
                    row[15] = None      
                db.session.add(Data(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 
                                    row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18]))
        db.session.commit()
        
    
    lg.warning('Database initialized!')
