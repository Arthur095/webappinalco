import os
#usr:mdp@ip/database
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://tp:tp@localhost/geoname'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#Hash Key
SECRET_KEY = "13123CQCQQDCQDQDQZD24223HQfqdqadjduoihéo&7"
#Type du token pour l'authentification JWT
JWT_AUTH_HEADER_PREFIX = 'BEARER'
#Url
Base_URL = "digidata.api.localhost"