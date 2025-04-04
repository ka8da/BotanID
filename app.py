from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import sqlite3
import posts

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts=all_posts)

@app.route("/find_post")
def find_post():
    query = request.args.get("query")
    if query:
        results = posts.find_posts(query)
    else:
        query = ""
        results = []
    return render_template("find_post.html", query=query, results=results)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    return render_template("show_post.html", post=post)

@app.route("/new_post")
def new_post():
    return render_template("new_post.html")

@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]

    posts.add_post(title, description, user_id)

    return redirect("/")

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    post = posts.get_post(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/update_post", methods=["POST"])
def update_post():
    post_id = request.form["post_id"]
    title = request.form["title"]
    description = request.form["description"]

    posts.update_post(post_id, title, description)

    return redirect("/post/" + str(post_id))

@app.route("/remove_post/<int:post_id>", methods=["GET", "POST"])
def remove_post(post_id):
    if request.method == "GET":
        post = posts.get_post(post_id)
        return render_template("remove_post.html", post=post)

    if request.method == "POST":
        if "remove" in request.form:
            posts.remove_post(post_id)
            return redirect("/")
        else:
            return redirect("/post/" + str(post_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: the passwords don't match"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username is already taken"

    return "Success"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: wrong password or username"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")