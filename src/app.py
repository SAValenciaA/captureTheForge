from flask import Flask, request, escape
import theForge

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.route("/dashboard")
def home():
    return "<p>Hello, World!</p>"


@app.route("/login")
def login():
    return "<p>Hello, World!</p>"

@app.route("/register")
def register():
    return "<p>Hello, World!</p>"

@app.route("/play")
def play():
    return render_template("play.html", puzzles=puzzles)

@app.route("/api/play")
def apiPlay():
    puzzleID = request.args.get("id", "Flask")
    return f"You requested for {puzzleID}"

@app.route("/api/addPuzzle")
def apiPlay():
    puzzleID = request.args.get("id", "Flask")
    return f"You requested for {puzzleID}"
