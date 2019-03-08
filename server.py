from flask import *
import sqlite3 as sqlite
app = Flask(__name__)
import random

with sqlite.connect("database.db") as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users(username, password);")

@app.route("/login",  methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite.connect("database.db") as conn:
            cur = conn.cursor()
            results = cur.execute("SELECT username FROM users WHERE username=? AND password=?;", (username,password)).fetchone()
        if results == None:
            return render_template("gnom.html")
        else:
            return render_template("index.html", name=" " + results[0])
    else: #method is get
        return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite.connect("database.db") as conn:
            cur = conn.cursor()
            results = cur.execute("SELECT username FROM users WHERE username=? AND password=?;", (username,password)).fetchone()
        if results == None:
            with sqlite.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users VALUES (?,?);", (username, password))
                conn.commit()
            return render_template("index.html", name=" " + results)
        else:
            return render_template("index.html", name=" " + username)

@app.route("/smoke", methods=["GET", "POST"])
def smoke():
    themes = open("themes.txt", "r")
    themes = themes.readlines()
    theme = themes[random.randint(0, 95)]
    shows = open("show.txt", "r")
    shows = shows.readlines()
    show = shows[random.randint(0, 48)]
    quotes = open("quotes.txt", "r")
    quotes = quotes.readlines()
    quote = quotes[random.randint(0, 7)]

    result = "The line '" + quote + "' does " + show + " the theme of " + theme


    return render_template("smoked.html", smoke=result)

@app.route("/saved", methods=["GET", "POST"])
def saved():
    with sqlite.connect("smokes.db") as acs:
        cur = acs.cursor()
        results = cur.execute("SELECT * FROM saved;").fetchall()
    return render_template("saved.html", saved=results)

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", name="")

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html", name="")

@app.route("/test", methods=["GET", "POST"])
def test():
    with sqlite.connect("database.db") as conn:
        cur = conn.cursor()
        results = cur.execute("SELECT * FROM users;").fetchall()
    return str(results)

app.run(debug=True)
