# blog-prototype

This was one of my first projects to pratice Flask and SQL.

It's a twitter-like blog where users can write, edit and delete posts.
The features include registration, login, logout, change username, email and profile pic and also has e password reset function.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages needed to run the application.

```bash
pip install -r requirements.txt
```

## Usage


To run the application you will need a .env file. There is a .env_example file in the project that has all the environment variables that you'll need:
```
SQLALCHEMY_DATABASE_URI → The database URI (it can be 'sqlite:///site.db'  to run locally)
SECRET_KEY= A hex string

# The variables below configure the email client that will be used to send the password reset token.
MAIL_SERVER= 
MAIL_PORT=
MAIL_USE_TLS=
EMAIL_USER=
EMAIL_PASS=
```

With the .env file ready all you need is to execute the 'run.py' file. If you are running locally with sqlite as the db, the sqlite file will be created inside the 'app' folder.

