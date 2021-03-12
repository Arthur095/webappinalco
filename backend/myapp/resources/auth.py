from backend.myapp import *
from backend.myapp.services.UserService import UserService

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('auth/register.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('data/search.html')