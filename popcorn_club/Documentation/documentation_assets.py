"""Compile static assets."""
from flask_assets import Bundle

documentation_style_bundle = Bundle(
    'documentation_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/documentation.min.css'
)