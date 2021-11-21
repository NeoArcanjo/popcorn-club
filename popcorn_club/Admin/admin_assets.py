"""Compile static assets."""
from flask_assets import Bundle

admin_bundles = {
    "admin_js": Bundle('admin_bp/src/js/*.js',
                       filters="jsmin",
                       output="dist/js/admin.%(version)s.js"),
    "admin_style": Bundle('admin_bp/src/css/*.css',
                          filters='cssmin',
                          output='dist/css/admin.%(version)s.css')
}
