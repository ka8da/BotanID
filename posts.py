import db

def get_post(post_id):
    sql ="""SELECT  posts.id,
                    posts.title,
                    posts.image,
                    posts.description,
                    posts.topic,
                    users.username,
                    users.id as user_id
            FROM    posts, users
            WHERE   posts.user_id = users.id AND
                    posts.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def add_post(title, image, description, topic, user_id):
    sql = "INSERT INTO posts (title, image, description, topic, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, image, description, topic, user_id])

def get_posts():
    sql = "SELECT id, title FROM posts ORDER BY id DESC"
    return db.query(sql)

def update_post(post_id, title, image, description, topic):
    sql = """UPDATE posts   SET title = ?,
                                image = ?,
                                description = ?,
                                topic = ?
                            WHERE id = ?"""
    db.execute(sql, [title, image, description, topic, post_id])

def remove_post(post_id):
    sql = "DELETE FROM posts WHERE id = ?"
    db.execute(sql, [post_id])

def find_posts(query):
    sql = """   SELECT id, title
                FROM posts
                WHERE description LIKE ? OR title LIKE ?
                ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def get_by_topic(topic):
    sql = "SELECT topic FROM posts WHERE topic = ? ORDER BY id"
    return db.query(sql, [topic])