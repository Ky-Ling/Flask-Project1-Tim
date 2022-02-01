'''
Date: 2021-11-05 13:22:27
LastEditors: GC
LastEditTime: 2021-11-25 10:38:50
FilePath: \Flask-Blog-Project1 Tim\website\models.py
'''

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# One to many relationship: One user has many posts, comments and likes, one post has many comments and likes


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(
        timezone=True), default=func.now())
    posts = db.relationship("Post", backref="user", passive_deletes=True)
    comments = db.relationship("Comment", backref="user", passive_deletes=True)
    likes = db.relationship("Like", backref="user", passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(
        timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    # db.ForeignKey("user.id") --> Put the name and the field of the table that this foreign key is going to reference.
    # ondelete="CASCADE" --> It means when i deleted the user of this table(Post) is referencing, i wanna cascade and delete all of the post that this user has
    #   so it just makes sure if the user get deleted, all the post of the user has get deleted as well.
    comments = db.relationship(
        "Comment", cascade='all, delete-orphan', backref="post")
    likes = db.relationship("Like", backref="post", passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(
        timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post.id", ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(
        timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        "post.id", ondelete="CASCADE"), nullable=False)
