from flask import Flask, render_template, redirect, request, session, flash, send_from_directory, url_for
from models import Users
from config import db, app
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'png'])


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
    return render_template("dashboard.html")


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

