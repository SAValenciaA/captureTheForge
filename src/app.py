import os
import users
import puzzles
import hashlib
import categories
import database
import hashTable
from werkzeug.utils import secure_filename
from flask import Flask, request, g, render_template, redirect, url_for, jsonify, make_response, send_from_directory, current_app

app = Flask(__name__)
md5 = lambda password: hashlib.md5(password.encode()).hexdigest()

ALLOWED_EXTENSIONS = {'zip'}

database.init_db(app)

app.config['UPLOAD_FOLDER'] = '../puzzles_files'
app.flags = None

@app.before_request
def load_flags():
    puzzles_flags = database.query("select id, flag from Puzzles")
    flags = hashTable.HashTable(len(puzzles_flags))
    for puzzle in puzzles_flags:
        flags.insert(puzzle['id'], puzzle['flag'])

    current_app.flags = flags


@app.route("/")
def home():
    return render_template('home.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'extraFiles' not in request.files:
            print("No file sent")
            print(request.files)
            return ''
        file = request.files['extraFiles']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print("nameless file")
            return ''

        if file and allowed_file(file.filename):
            print("saving file")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    #if not request.method in ["POST", "GET"]:
    #    return "<h1>HAZAAAAHHHHH.<\\ h1>"

    if request.method == "POST":
        name = request.form['name'] 
        flag = request.form['flag']
        tags = request.form['tags']
        description = request.form['description']
        extraFiles = save_file(request)
        dificulty = request.form['dificulty']

        puzzles.Puzzle.create_puzzle(name, flag, tags, description, extraFiles, dificulty)

        return redirect(url_for('dashboard'))

    if request.method == "GET":
        return render_template('dashboard.html')

@app.route("/api/check_flag", methods=["POST"])
def check_flag():
    flag_id = request.form['id']
    user_answer = request.form['flag']
    if current_app.flags.search(flag_id) != md5(user_answer ):
        return jsonify({
            'status': 'failure',
            'message': 'The flag given is incorrect.'
        })

    auth_cookie = request.cookies.get('auth').split(":")
    username = auth_cookie[0]
    user = users.User.get_user("name", username)

    puzzle = puzzles.Puzzle.get_puzzle("id", flag_id)

    user.score += puzzle.dificulty
    user.solves += puzzle.id + ","
    print(f"{user.score}:{user.solves}")

    user.save(app.scoreboard)

    return jsonify({
        'status': 'success',
        'message': 'Correct!'
    })

@app.before_request
def load_scoreboard():
    users_list = database.query("select * from Users limit 50")
    scoreboard = users.ScoreBoard()
    for user in users_list:
        new_user = users.User(user)
        scoreboard.insert(new_user)


    current_app.scoreboard = scoreboard

@app.route("/scoreboard")
def scoreboard():
    return render_template("scoreboard.html", users=app.scoreboard)



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
    puzzle_id = request.args.get('id')

    if puzzle_id:
        puzzle = puzzles.Puzzle.get_puzzle("id", puzzle_id)
        return render_template('puzzle.html', puzzle=puzzle)
    else:
        puzzles_list = puzzles.Puzzle.get_puzzle_list()
        return render_template('play.html', puzzles=puzzles_list)


@app.route("/api/login", methods=['POST'])
def api_login_user():

    if request.method != "POST":
        return "<h1>HAZAAAAHHHHH.<\\ h1>"

    username = request.form['name'] 
    password = request.form['password']

    pressumed_user = users.User.get_user("name", username)

    if pressumed_user == None:
        response = {'status': 'error', 'message': 'Username or password wrong'}
        return jsonify(response)

    password_hash = md5(password)

    if password_hash != pressumed_user.password:
        response = {'status': 'error', 'message': 'Username or password wrong'}
        return jsonify(response)

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

@app.route('/download/<path:filename>')
def download(filename):
    print(filename)
    print(app.config['UPLOAD_FOLDER'])
    return send_from_directory(app.config['UPLOAD_FOLDER'],path=filename, as_attachment=True)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.before_request
def load_categories():

    puzzles_list = [
        puzzles.Puzzle(puzzle_data) 
        for puzzle_data in database.query("select * from Puzzles")
    ]

    categories_list = categories.Categories()

    for puzzle in puzzles_list:
        tags_list = puzzle.tags.split(",")
        categories_list.add(tags_list, puzzle)

    current_app.categories = categories_list

@app.route('/search', methods=['GET'])
def search():

    if main_tag := request.args.get('main_category'):
        print("first")
        main_tag = app.categories.head.find(main_tag)

    if secundary_tag := request.args.get('secundary_category'):
        print("scond")
        secundary_tag = main_tag.find(secundary_tag)

    if terceary_tag := request.args.get('terceary_category'):
        print("third")
        terceary_tag = secundary_tag.find(terceary_tag)


    return render_template(
        'search.html',
        main_category=main_tag,
        secundary_category=secundary_tag,
        terceary_category=terceary_tag,
        categories=app.categories
    )


