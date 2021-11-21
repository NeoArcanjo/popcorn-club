"""Compile static assets."""
from flask_assets import Bundle

admin_style_bundle = Bundle(
    'admin_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/admin.min.css'
)