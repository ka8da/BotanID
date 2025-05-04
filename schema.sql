CREATE TABLE "users" ("id" INTEGER PRIMARY KEY, "username" TEXT UNIQUE, "password_hash" TEXT);

CREATE TABLE "posts" ("id" INTEGER PRIMARY KEY, "title" TEXT, "description" TEXT, "topic" TEXT CHECK(topic IN ("Plant ID", "Plant care", "Plant hospital")) "image" BLOB, "user_id" INTEGER REFERENCES "users"("id"))

CREATE TABLE "comments" ("id" INTEGER PRIMARY KEY UNIQUE, "post_id" INTEGER REFERENCES "posts"("id"), "user_id" INTEGER REFERENCES "users"("id"), "comment" TEXT)