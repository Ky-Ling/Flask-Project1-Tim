'''
Date: 2021-11-04 13:57:06
LastEditors: GC
LastEditTime: 2021-11-16 20:24:46
FilePath: \Flask-Blog-Project\website\auth.py
'''
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user:
            # Check whether the password the user typed in is equal to the password that was stored in the user model.
            if check_password_hash(user.password, password):
                flash("Logged in!!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect!!", category="error")
        else:
            flash("Email does not exist!", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        # Validation
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email is already in use. ", category="error")
        elif username_exists:
            flash("User name is already in use. ", category="error")
        elif password1 != password2:
            flash("Password don\'t match! Please try again.", category="error")
        elif len(username) < 2:
            flash("User name is too short!", category="error")
        elif len(password1) < 6:
            flash("Password is too short!", category="error")
        else:
            # Create the new user:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method="sha256"))

            # Add this new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the user after we creating the account
            login_user(new_user, remember=True)
            flash("User created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


# With this decorator, means we can only access this logout page if we have been logged in
@login_required
@auth.route("/logout")
def logout():
    logout_user()

    # Redirect the user to the home function of views.py
    return redirect(url_for("views.home"))
