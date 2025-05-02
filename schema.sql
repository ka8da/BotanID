CREATE TABLE "users" (`id` INTEGER PRIMARY KEY, `username` TEXT UNIQUE, `password_hash` TEXT);

CREATE TABLE "posts" (`id` INTEGER PRIMARY KEY, `title` TEXT, `description` TEXT, `topic` TEXT, `image` BLOB, `user_id` INTEGER REFERENCES `users`(`id`))