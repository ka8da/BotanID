from flask import Flask, abort, redirect, render_template, request, session
import config
import db
import sqlite3
import posts
import users
import base64

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts=all_posts)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    posts = users.get_users_posts(user_id)
    return render_template("show_user.html", user=user, posts=posts)

ALLOWED_TOPICS = {"Plant ID", "Plant care", "Plant hospital"}

@app.route("/posts_by_topic")
def posts_by_topic(topic):
    topic = posts.get_by_topic(topic)
    if not topic:
        abort(404)
    return render_template("topics.html", topic=topic)

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
    if not post:
        abort(404)
    return render_template("show_post.html", post=post)

@app.route("/new_post")
def new_post():
    return render_template("new_post.html")

@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form["title"]
    if len(title) > 50:
        abort(403)

    image = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            image = file.read()

    description = request.form["description"]
    if len(description) > 1000:
        abort(403)

    topic = request.form["topic"]
    if topic not in ALLOWED_TOPICS:
        abort(403)
    user_id = session["user_id"]

    posts.add_post(title, image, description, topic, user_id)
    return redirect("/")

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_post.html", post=post)

@app.route("/update_post", methods=["POST"])
def update_post():
    require_login()
    post_id = request.form["post_id"]
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)

    remove_image = 'remove_image' in request.form
    new_image = None
    
    if 'new_image' in request.files:
        file = request.files['new_image']
        if file.filename != '':
            new_image = file.read()
    
    if remove_image:
        final_image = None
    elif new_image:
        final_image = new_image
    else:
        final_image = post["image"]
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    topic = request.form["topic"]
    if topic not in ALLOWED_TOPICS:
        abort(403)

    posts.update_post(post_id, title, final_image, description, topic)
    return redirect("/post/" + str(post_id))

@app.route("/remove_post/<int:post_id>", methods=["GET", "POST"])
def remove_post(post_id):
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "ERROR: Username is already taken"
    
    return "Success"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: wrong password or username"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")