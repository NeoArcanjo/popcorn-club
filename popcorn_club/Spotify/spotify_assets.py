"""Compile static assets."""
from flask_assets import Bundle

Bundle('spotify_bp/src/scss/*.scss', filters='pyscss',
       output='dist/css/spotify.%(version)s.css')

spotify_bundles = {
    "spotify_js": Bundle('spotify_bp/src/js/*.js',
                         filters="jsmin",
                         output="dist/js/spotify.%(version)s.js"),
    "spotify_style": Bundle('spotify_bp/src/css/*.css',
                            filters='cssmin',
                            output='dist/css/spotify.%(version)s.css')
}
