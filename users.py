from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user(user_id):
    sql ="SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_users_posts(user_id):
    sql = """SELECT posts.id,
                    posts.title,
                    posts.description,
                    posts.topic,
                    posts.image,
                    COUNT(comments.id) as comment_count
            FROM posts
            LEFT JOIN comments ON comments.post_id = posts.id
            WHERE posts.user_id = ?
            GROUP BY posts.id, posts.title, posts.description, 
                    posts.topic, posts.image
            ORDER BY posts.id DESC"""
    return db.query(sql, [user_id])

def create_user(username, password1):
    password_hash = generate_password_hash(password1)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
