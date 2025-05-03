# BotanID

## Purpose of the application

BotanID is a houseplant-related social media application.

Here you can share pictures of your mystery plants, ask others for advice, and gain expertise.

* Users can create accounts and log into the application
* Users can add, edit and remove posts
* Users can add photos to the posts
* Users can pick whether the post fits under different categories (identification, care advice, and help with bug infestations)
* Users can search for posts
* Users can see each others' posts
* Users can comment on others' posts
* Application has a home page and users' profile pages

## Installation

Install `flask`-library:

```
$ pip install flask
```

Create database tables and initialize:

```
$ sqlite3 database.db < schema.sql
```

Run the application:

```
$ flask run
```

