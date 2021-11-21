"""Compile static assets."""
from flask_assets import Bundle

dashboard_style_bundle = Bundle(
    'dashboard_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/dashboard.min.css'
)