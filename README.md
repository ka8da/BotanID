# BotanID

## Purpose of the application

BotanID is a plant identification social media application.

Here you can share pictures of your mystery plants and gain knowledge and advice.

Currently available features:
* Users can create accounts and log into the application
* Users can add, edit and remove posts
* Users can search for posts
* Users can see each others' posts


Features that will be added:
* Users can add photos to the posts
* Users can comment on others' posts and like comments
* Application has a home page and users' private profile pages
* Users can pick top comments of their posts
* Users can pick whether the post fits under different categories (identification, care advice, diy ideas, etc.)


## Installation

Install `flask`-library:

```
$ pip install flask
```

Create database tables and initialize:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Run the application:

```
$ flask run
```

