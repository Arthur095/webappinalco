from backend.myapp import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('auth/register.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('data/search.html')