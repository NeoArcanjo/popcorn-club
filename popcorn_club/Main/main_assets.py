"""Compile static assets."""
from flask_assets import Bundle

main_bundles = {
    "main_js": Bundle('main_bp/src/js/*.js',
                      filters="jsmin",
                      output="dist/js/main.%(version)s.js"),
    "main_style": Bundle('main_bp/src/css/*.css',
                         filters='cssmin',
                         output='dist/css/main.%(version)s.css')
}
