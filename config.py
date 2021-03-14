import os
#usr:mdp@ip/database
#SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tp:tp@localhost/geoname'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://inaldb2.cfaotho2xsxm.us-east-2.rds.amazonaws.com:5432/geoname?user=postgres&password=elvis2021'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#Hash Key
SECRET_KEY = "d2JhIUWoomWtLCCC7dHWMo6Dil1gyhhsEG.UZHpfH4rNB239ay.GFvHEvhQLLrMry2TRkLNzHx25ICgLbpJ3yb0twfkTxMtRiocP"
#Type du token pour l'authentification JWT
JWT_AUTH_HEADER_PREFIX = 'BEARER'
#Url
Base_URL = "digidata.api.localhost"