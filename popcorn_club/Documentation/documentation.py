import os
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask import current_app as app
from popcorn_club.Auth.auth import login_required

documentation_bp = Blueprint('documentation_bp', __name__, url_prefix='/documentation',
               template_folder='templates', static_folder='static')


@documentation_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


@documentation_bp.route("/buttons")
@login_required
def buttons():
    return render_template('buttons.html')


@documentation_bp.route("/cards")
@login_required
def cards():
    return render_template('cards.html')


@documentation_bp.route("/utilities-color")
@login_required
def utilities_color():
    return render_template('utilities-color.html')


@documentation_bp.route("/utilities-border")
@login_required
def utilities_border():
    return render_template('utilities-border.html')


@documentation_bp.route("/utilities-animation")
@login_required
def utilities_animation():
    return render_template('utilities-animation.html')


@documentation_bp.route("/utilities-other")
@login_required
def utilities_other():
    return render_template('utilities-other.html')


@documentation_bp.route("/charts")
@login_required
def charts():
    return render_template('charts.html')


@documentation_bp.route("/tables")
@login_required
def tables():
    return render_template('tables.html')
