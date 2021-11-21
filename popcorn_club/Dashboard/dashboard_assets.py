"""Compile static assets."""
from flask_assets import Bundle

dashboard_bundles = {
    "dashboard_js": Bundle('dashboard_bp/src/js/*.js', 'dashboard_bp/src/vendor/*/*.js',
                           filters="jsmin",
                           output="dist/js/dashboard.%(version)s.js"),
    "dashboard_style": Bundle('dashboard_bp/src/css/*.css',
                              filters='cssmin',
                              output='dist/css/dashboard.%(version)s.css')
}
