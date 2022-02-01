'''
Date: 2021-11-04 13:47:53
LastEditors: GC
LastEditTime: 2021-11-16 16:24:37
FilePath: \Flask-Blog-Project\website\__init__.py
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


class Config:
    SECRET_KEY = "helloworld"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


def create_app():
    app = Flask(__name__)

    # Load the configure information before we initial the app
    app.config.from_object(Config)
    Config.init_app(app)

    # app.config["SECRET_KEY"] = "helloworld"
    # app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import the blueprint and register that blueprint
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Before we create our database, we need to import all the models individually that we want to be created in our database.
    from .models import User, Post, Comment, Like
    create_database(app)

    # New we created our database, we need to set up the login manager
    login_manager = LoginManager()

    # When someone tries to access a page and they are not logged in, we should redirect them to the login page
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Create a function so that our log-in manager can actually find our user model when it logs in.
    @login_manager.user_loader
    def load_user(id):
        # This function is allow me to access the information related to the user from the my database, giving the id of the user.
        return User.query.get(int(id))

    return app


def create_database(app):
    if path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!!")
