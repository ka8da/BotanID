CREATE TABLE "posts" (`id` INTEGER PRIMARY KEY, `title` TEXT, `description` TEXT, `user_id` INTEGER REFERENCES `users`(`id`));

CREATE TABLE "users" (`id` INTEGER PRIMARY KEY, `username` TEXT UNIQUE, `password_hash` TEXT);