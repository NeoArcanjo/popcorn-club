"""Compile static assets."""
from flask_assets import Bundle

auth_style_bundle = Bundle(
    'auth_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/auth.min.css'
)