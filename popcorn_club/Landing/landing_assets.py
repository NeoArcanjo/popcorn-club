"""Compile static assets."""
from flask_assets import Bundle

landing_style_bundle = Bundle(
    'landing_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/landing.css'
)