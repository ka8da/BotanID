import db

def get_post(post_id):
    sql ="""SELECT  posts.id,
                    posts.title,
                    posts.description,
                    users.username,
                    users.id as user_id
            FROM    posts, users
            WHERE   posts.user_id = users.id AND
                    posts.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def add_post(title, description, user_id):
    sql = "INSERT INTO posts (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def update_post(post_id, title, description):
    sql = """UPDATE posts   SET   title = ?,
                                description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, post_id])
