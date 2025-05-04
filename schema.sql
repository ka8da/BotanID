CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY,
    "username" TEXT UNIQUE,
    "password_hash" TEXT
);

CREATE INDEX idx_users_username ON users(username);

CREATE TABLE "posts" (
    "id" INTEGER PRIMARY KEY,
    "title" TEXT,
    "description" TEXT,
    "topic" TEXT CHECK(topic IN ("Plant ID", "Plant care", "Plant hospital")),
    "image" BLOB,
    "user_id" INTEGER REFERENCES "users"("id"),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_topic ON posts(topic);
CREATE INDEX idx_posts_created ON posts(created_at);

CREATE TABLE "comments" (
    "id" INTEGER PRIMARY KEY,
    "post_id" INTEGER REFERENCES "posts"("id"),
    "user_id" INTEGER REFERENCES "users"("id"),
    "comment" TEXT,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_post_user ON comments(post_id, user_id);