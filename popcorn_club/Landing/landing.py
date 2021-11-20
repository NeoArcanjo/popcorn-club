import os
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask import current_app as app
from popcorn_club.Auth.auth import login_required

landing_bp = Blueprint('landing_bp', __name__, url_prefix='/landing',
               template_folder='templates', static_folder='static')


@landing_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


@landing_bp.route("/buttons")
@login_required
def buttons():
    return render_template('buttons.html')


@landing_bp.route("/cards")
@login_required
def cards():
    return render_template('cards.html')


@landing_bp.route("/utilities-color")
@login_required
def utilities_color():
    return render_template('utilities-color.html')


@landing_bp.route("/utilities-border")
@login_required
def utilities_border():
    return render_template('utilities-border.html')


@landing_bp.route("/utilities-animation")
@login_required
def utilities_animation():
    return render_template('utilities-animation.html')


@landing_bp.route("/utilities-other")
@login_required
def utilities_other():
    return render_template('utilities-other.html')


@landing_bp.route("/charts")
@login_required
def charts():
    return render_template('charts.html')


@landing_bp.route("/tables")
@login_required
def tables():
    return render_template('tables.html')
