from flask import Flask, render_template, redirect, request, session, flash, send_from_directory, url_for
from models import Users, Channels
from config import db, app
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'png'])
PUBLIC_CHANNEL = 1
PRIVATE_CHANNEL = 2


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
    public_channels = Channels.get_public_channels()

    private_channels = Channels.query.filter_by(id=PRIVATE_CHANNEL)
    owned_channels = Channels.get_owned_channels(current_user.id)

    return render_template("dashboard_test.html", user=current_user,public_channels=public_channels,
                           owned_channels=owned_channels)


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


def show_channels_page():
    print(f"ROUTE: show_channels_page")
    if 'user_id' not in session:
        print(f"User id not found")
        return redirect('/')

    current_user = Users.query.get(session['user_id'])

    public_channels = Channels.get_public_channels()

    private_channels = Channels.query.filter_by(id=PRIVATE_CHANNEL)
    owned_channels = Channels.get_owned_channels(current_user.id)

    return render_template("channels_test.html", user=current_user, public_channels=public_channels,
                           owned_channels=owned_channels)


def create_new_channel():
    print(f"ROUTE: create_new_channel")
    print(f"Adding new channel")
    print(f"Channel form: {request.form}")

    current_user = Users.query.get(session['user_id'])

    if request.form['options'] == "public":
        channel_type = PUBLIC_CHANNEL
    else:
        channel_type = PRIVATE_CHANNEL

    channel_id = Channels.add_new_channel(current_user.id, request.form['channel_title'],
                                          request.form['channel_description'], channel_type)

    return redirect(url_for("show_channels_page"))


def show_channel_messages(channel_id):
    return render_template("channel_messages.html")
