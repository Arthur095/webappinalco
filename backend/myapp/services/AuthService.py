from werkzeug.security import safe_str_cmp

"""Classe utilisateur pour l'authentification, on rajoute ces objets dans une liste de paire user/password, ici en brut mais qui peut être lue depuis un fichier ou une db"""
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

"""Compare le token du header de la requête avec celui généré"""
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

"""Renvoie l'indice de l'utlisateur dans la list users de l'utilisateur s'étant connecté."""
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

#users enregistrés
users = [
    User(1, 'admin', 'admin'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}