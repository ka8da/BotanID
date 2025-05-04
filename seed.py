import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM posts")
db.execute("DELETE FROM comments")

user_count = 100
post_count = 10**2
comment_count = 10**2
topics = ["Plant ID", "Plant care", "Plant hospital"]

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
                ["user" + str(i)])

for i in range(1, post_count + 1):
    user_id = random.randint(1, user_count)
    topic = random.choice(topics)
    db.execute("INSERT INTO posts (title, description, topic, user_id) VALUES (?, ?, ?, ?)",
               ["title" + str(i), "description" + str(i), topic, user_id])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    post_id = random.randint(1, post_count)
    db.execute("INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)",
               [post_id, user_id, "comment" + str(i)])

db.commit()
db.close()
