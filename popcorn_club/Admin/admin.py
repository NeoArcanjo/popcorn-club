import os
from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from flask import current_app as app
from popcorn_club.Auth.auth import login_required

theme="default"

bp = Blueprint('admin2', __name__, url_prefix='/admin',
               template_folder=f'templates/{theme}', static_folder='static')


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(f'crm-dashboard.html')


@bp.route("/buttons")
@login_required
def buttons():
    return render_template('buttons.html')


@bp.route("/cards")
@login_required
def cards():
    return render_template('cards.html')


@bp.route("/utilities-color")
@login_required
def utilities_color():
    return render_template('utilities-color.html')


@bp.route("/utilities-border")
@login_required
def utilities_border():
    return render_template('utilities-border.html')


@bp.route("/utilities-animation")
@login_required
def utilities_animation():
    return render_template('utilities-animation.html')


@bp.route("/utilities-other")
@login_required
def utilities_other():
    return render_template('utilities-other.html')


@bp.route("/charts")
@login_required
def charts():
    return render_template('charts.html')


@bp.route("/tables")
@login_required
def tables():
    return render_template('tables.html')
