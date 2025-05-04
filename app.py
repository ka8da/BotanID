from flask import Flask
from flask import abort, redirect, render_template, request, session, url_for
import config, db, posts, users
import sqlite3, base64, secrets
import time
from flask import g

app = Flask(__name__)
app.secret_key = config.secret_key
ALLOWED_TOPICS = {"Plant ID", "Plant care", "Plant hospital"}

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

def require_login():
    if "user_id" not in session:
        session['next_url'] = request.url
        return redirect(url_for('register'))

def check_csrf():
    if "csrf_token" not in session:
        abort(403)

    if request.method != "POST":
        abort(405)

    if "csrf_token" not in request.form:
        abort(403)

    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 48

    posts_to_show = posts.get_posts(page=page, per_page=per_page)

    total_posts = posts.get_total_post_count()
    total_pages = (total_posts + per_page -1) // per_page

    if page < 1:
        return redirect(url_for('index', page=1))
    if page > total_pages and total_pages > 0:
        return redirect(url_for('index', page=total_pages))

    return render_template(
        "index.html",
        posts=posts_to_show,
        page=page,
        total_pages=total_pages
    )

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    user_posts = users.get_users_posts(user_id)
    comment_count = posts.get_comment_count_by_user(user_id)

    return render_template(
        "show_user.html",
        user=user,
        posts=user_posts,
        comment_count=comment_count)

@app.route("/posts_by_topic/<topic>")
def posts_by_topic(topic):
    if topic not in ALLOWED_TOPICS:
        abort(404)

    page = request.args.get("page", 1, type=int)
    per_page = 48
    
    posts_to_show = posts.get_by_topic(topic, page=page, per_page=per_page)

    total_posts = posts.get_post_count_by_topic(topic)
    total_pages = (total_posts + per_page - 1) // per_page

    if page < 1:
        return redirect(url_for('posts_by_topic', topic=topic, page=1))
    if page > total_pages and total_pages > 0:
        return redirect(url_for('posts_by_topic', topic=topic, page=total_pages))

    return render_template(
        "topics.html",
        posts=posts_to_show, 
        topic=topic,
        page=page,
        total_pages=total_pages)

@app.route("/find_post")
def find_post():
    query = request.args.get("query", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 48
    
    if query:
        results = posts.search_posts(query, page=page, per_page=per_page)
        total_results = posts.get_search_count(query)
        total_pages = (total_results + per_page - 1) // per_page
    else:
        results = []
        total_pages = 0
    
    return render_template(
        "find_post.html",
        query=query,
        results=results,
        page=page,
        total_pages=total_pages)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    comments = posts.get_comments(post_id)
    comment_count = posts.get_comment_count(post_id)
    return render_template("show_post.html", post=post, comments=comments, comment_count=comment_count)

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

    post_id = db.last_insert_id()
    return redirect("/post/" + str(post_id))

@app.route("/edit_post/<int:post_id>")
def edit_post(post_id):
    check_csrf()
    require_login()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_post.html", post=post)

@app.route("/update_post", methods=["POST"])
def update_post():
    check_csrf()
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
    check_csrf()
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

@app.route("/comment", methods=["POST"])
def comment():
    check_csrf()
    require_login()
    if not request.form["comment"] or len(request.form["comment"]) > 1000:
        abort(400)
    comment = request.form["comment"]
    post_id = request.form["post_id"]
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    user_id = session["user_id"]

    posts.comment(post_id, user_id, comment)
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
        next_url = session.pop("next_url", None)
        return redirect(next_url or url_for("index"))
    
    except sqlite3.IntegrityError:
        return "ERROR: Username is already taken"

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
            session["csrf_token"] = secrets.token_hex(16)
            session["username"] = username
            return redirect("/")
        else:
            return "ERROR: wrong password or username"

@app.route("/logout")
def logout():
    require_login()
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
