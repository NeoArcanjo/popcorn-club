"""Compile static assets."""
from flask_assets import Bundle

spotify_style_bundle = Bundle(
    'spotify_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/spotify.css'
)