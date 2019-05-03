from flask import Flask, render_template, redirect, request, session, flash, send_from_directory, url_for
from models import Users, Articles
from config import db, app
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'png'])
PUBLIC_CHANNEL = 1
PRIVATE_CHANNEL = 2


# posts = [
#     {
#         'author': 'Rick Brown',
#         'title': 'My First Blog',
#         'content': 'Blah blah blah blah',
#         'date_posted': 'April 29, 2019'
#     },
# {
#         'author': 'Rick Brown',
#         'title': 'My Second Blog',
#         'content': 'Blah blah blah blah',
#         'date_posted': 'April 30, 2019'
#     },
# {
#         'author': 'Jessie Miles',
#         'title': 'My First Blog',
#         'content': 'Yadda yada yada',
#         'date_posted': 'April 30, 2019'
#     }
# ]


def index():
    print(f"ROUTE: index")
    return render_template("index.html")


def show_register_page():
    print(f"ROUTE: register")
    return render_template("register.html")


def process_new_user():
    print(f"ROUTE: process_new_user")
    errors = Users.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect('/register')

    user_id = Users.create(request.form)
    session['user_id'] = user_id
    return redirect(url_for("show_dashboard"))


def show_dashboard():
    print(f"ROUTE: show_dashboard")
    if 'user_id' not in session:
        print(f"User id not found")
        return redirect('/')

    current_user = Users.query.get(session['user_id'])
    posts = Articles.get_latest_articles()
    posts.reverse()

    return render_template("dashboard.html", user=current_user, posts=posts)


def show_login_page():
    print(f"ROUTE: show_dashboard")
    return render_template("login.html")


def login():
    print(f"ROUTE: login: {request.form}")
    valid, response = Users.login_validate(request.form)

    if not valid:
        flash(response)
        return redirect('/login')
    session['user_id'] = response
    return redirect(url_for("show_dashboard"))


def users_logout():
    print(f"ROUTE: logout")
    session.clear()
    return redirect('/')


def show_post_form():
    print(f"ROUTE: show_post_form")
    current_user = Users.query.get(session['user_id'])

    return render_template("posts.html", user=current_user)


def post_article():
    print(f"ROUTE: post_article")
    print(f"Form Data: {request.form}")
    article_id = Articles.add_to_db(request.form, session['user_id'])
    return redirect(url_for("show_dashboard"))
