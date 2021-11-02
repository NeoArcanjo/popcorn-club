import os
from flask import Flask, render_template, request, redirect, url_for, session
from films.functions import get_data, base_url, img_url, login_required
from src.main import app, oauth

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('admin/index.html')


@app.route("/buttons")
@login_required
def buttons():
    return render_template('admin/buttons.html')


@app.route("/cards")
@login_required
def cards():
    return render_template('admin/cards.html')


@app.route("/utilities-color")
@login_required
def utilities_color():
    return render_template('admin/utilities-color.html')


@app.route("/utilities-border")
@login_required
def utilities_border():
    return render_template('admin/utilities-border.html')


@app.route("/utilities-animation")
@login_required
def utilities_animation():
    return render_template('admin/utilities-animation.html')


@app.route("/utilities-other")
@login_required
def utilities_other():
    return render_template('admin/utilities-other.html')


@app.route("/login2")
def login2():
    return render_template('admin/login.html')


@app.route("/register")
def register():
    return render_template('admin/register.html')


@app.route("/404")
def e404():
    return render_template('admin/404.html')


@app.route("/charts")
@login_required
def charts():
    return render_template('admin/charts.html')


@app.route("/tables")
@login_required
def tables():
    return render_template('admin/tables.html')


@app.route("/forgot-password")
@login_required
def forgot_password():
    return render_template('admin/forgot-password.html')


@app.route("/blank")
def blank():
    return render_template('admin/blank.html')

