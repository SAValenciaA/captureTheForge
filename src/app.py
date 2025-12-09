import users
import hashlib
from database import init_db
from flask import Flask, request, g, render_template, redirect, url_for, jsonify, make_response

app = Flask(__name__)
md5 = lambda password: hashlib.md5(password.encode()).hexdigest()

init_db(app)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/dashboard")
def dashboard():
    return "<p>Hello, World!</p>"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/play")
def play():

    auth_cookie = request.cookies.get('auth').split(":")
    username = auth_cookie[0]

    return f"<p>Let's play a game, {username}</p>"

@app.route("/api/play")
def api_play():
    puzzleID = request.args.get("id", "Flask")
    return f"You requested for {puzzleID}"


@app.route("/api/login", methods=['POST'])
def api_login_user():

    if request.method != "POST":
        return "<h1>HAZAAAAHHHHH.<\\ h1>"

    username = request.form['name'] 
    password = request.form['password']

    pressumed_user = users.User.get_user("name", username)

    if pressumed_user == None:
        response = {'status': 'error', 'message': 'Username or password wrong'}
        return jsonfy(response)

    password_hash = md5(password)

    if password_hash != pressumed_user.password:
        response = {'status': 'error', 'message': 'Username or password wrong'}
        return jsonfy(response)

    response = make_response(redirect(url_for('play')))
    response.set_cookie('auth', f'{username}:{password_hash}')

    return response

@app.route("/api/register", methods=['POST'])
def api_register_user():

    if request.method != "POST":
        return "<h1>That is not a valid method my dear boy.<\\ h1>"

    username = request.form['name'] 
    password = request.form['password']
    team = request.form['team']

    users.User.create_user(username, password, team)

    return redirect(url_for('login'))


@app.route("/api/addPuzzle")
def api_add_puzzle():
    puzzleID = request.args.get("id", "Flask")
    return f"You requested for {puzzleID}"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


