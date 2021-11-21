"""Compile static assets."""
from flask_assets import Bundle

auth_bundles = {
    "auth_js": Bundle('auth_bp/src/js/*.js',
                      filters="jsmin",
                      output="dist/js/auth.%(version)s.js"),
    "auth_style": Bundle('auth_bp/src/css/*.css',
                         filters='cssmin',
                         output='dist/css/auth.%(version)s.css')
}
