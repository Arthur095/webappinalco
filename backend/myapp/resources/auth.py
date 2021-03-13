from backend.myapp import *
from backend.myapp.services.UserService import UserService

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('auth/register.html')

@app.route('/search_data')
def search_data():
    return render_template('data/search_data.html')

@app.route('/search_users')
def search_users():
    return render_template('clients/search_users.html')