import db

def get_post(post_id):
    sql = """SELECT  posts.id,
                    posts.title,
                    posts.image,
                    posts.description,
                    posts.topic,
                    users.username,
                    users.id as user_id,
                    COUNT(comments.id) as comment_count
            FROM    posts
            JOIN    users ON posts.user_id = users.id
            LEFT JOIN comments ON comments.post_id = posts.id
            WHERE   posts.id = ?
            GROUP BY posts.id, posts.title, posts.image, 
                     posts.description, posts.topic, 
                     users.username, users.id"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def add_post(title, image, description, topic, user_id):
    sql = "INSERT INTO posts (title, image, description, topic, user_id) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [title, image, description, topic, user_id])

def get_posts(page=1, per_page=10):
    offset = (page - 1) * per_page
    sql = """SELECT posts.id,
                    posts.title,
                    posts.image,
                    posts.description,
                    posts.topic,
                    users.username,
                    users.id as user_id,
                    COUNT(comments.id) as comment_count
            FROM posts
            JOIN users ON posts.user_id = users.id
            LEFT JOIN comments ON comments.post_id = posts.id
            GROUP BY posts.id, posts.title, posts.image, 
                    posts.description, posts.topic, 
                    users.username, users.id
            ORDER BY posts.id DESC
            LIMIT ? OFFSET ?"""
    return db.query(sql, [per_page, offset])

def get_total_post_count():
    sql = "SELECT COUNT(*) FROM posts"
    result = db.query(sql)
    return result[0][0] if result else 0

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

def search_posts(query, page=1, per_page=10):
    offset = (page - 1) * per_page
    sql = """SELECT posts.id,
                    posts.title,
                    posts.description,
                    posts.topic,
                    users.username,
                    users.id as user_id,
                    COUNT(comments.id) as comment_count
            FROM posts
            JOIN users ON posts.user_id = users.id
            LEFT JOIN comments ON comments.post_id = posts.id
            WHERE posts.title LIKE ? OR posts.description LIKE ?
            GROUP BY posts.id, posts.title, posts.description, 
                    posts.topic, users.username, users.id
            ORDER BY posts.id DESC
            LIMIT ? OFFSET ?"""
    search_term = f"%{query}%"
    return db.query(sql, [search_term, search_term, per_page, offset])

def get_search_count(query):
    sql = """SELECT COUNT(DISTINCT posts.id)
             FROM posts
             WHERE posts.title LIKE ? OR posts.description LIKE ?"""
    search_term = f"%{query}%"
    result = db.query(sql, [search_term, search_term])
    return result[0][0] if result else 0

def comment(post_id, user_id, comment):
    sql = "INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [post_id, user_id, comment])

def get_comments(post_id):
    sql = """SELECT comments.comment, 
                    users.id user_id, 
                    users.username
             FROM comments, users
             WHERE comments.post_id = ? AND comments.user_id = users.id
             ORDER BY comments.id DESC"""
    return db.query(sql, [post_id])

def get_comment_count(post_id):
    sql = """SELECT COUNT(*) as comment_count 
             FROM comments 
             WHERE post_id = ?"""
    result = db.query(sql, [post_id])
    return result[0]["comment_count"] if result else 0

def get_comment_count_by_user(user_id):
    sql = """SELECT COUNT(*) as comment_count 
             FROM comments 
             WHERE user_id = ?"""
    result = db.query(sql, [user_id])
    return result[0]["comment_count"] if result else 0

def get_by_topic(topic, page=1, per_page=10):
    offset = (page - 1) * per_page
    sql = """SELECT posts.id,
                    posts.title,
                    posts.image,
                    posts.description,
                    posts.topic,
                    users.username,
                    users.id as user_id,
                    COUNT(comments.id) as comment_count
            FROM posts
            JOIN users ON posts.user_id = users.id
            LEFT JOIN comments ON comments.post_id = posts.id
            WHERE posts.topic = ?
            GROUP BY posts.id, posts.title, posts.image, 
                    posts.description, posts.topic, 
                    users.username, users.id
            ORDER BY posts.id DESC
            LIMIT ? OFFSET ?"""
    return db.query(sql, [topic, per_page, offset])

def get_post_count_by_topic(topic):
    sql = "SELECT COUNT(*) FROM posts WHERE topic = ?"
    result = db.query(sql, [topic])
    return result[0][0] if result else 0