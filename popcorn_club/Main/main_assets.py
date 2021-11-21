"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle

main_style_bundle = Bundle(
    'main_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/main.min.css'
)
