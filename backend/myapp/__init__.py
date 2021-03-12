import os, flask_login
from flask import Flask, render_template
from flask_jwt import JWT
from .services.AuthService import User, authenticate, identity
from werkzeug.security import safe_str_cmp

#Définition de l'app : Veuillez à importez les packages de l'app après.
app = Flask(__name__, static_folder= str(os.getcwd()) + '/frontend/static/', 
                    template_folder= str(os.getcwd()) + '/frontend/templates/')

# Config options - Soyez sur d'avoir créé un fichier 'config.py'.
app.config.from_object('config')
from . import models
from . import api
from .resources.auth import *


# Authorization avec Flask_JWT
jwt = JWT(app, authenticate, identity)

# Connection sqlalchemy à l'application
models.db.init_app(app)
models.init_db()

@app.cli.command()
def init_db():
    models.init_db()