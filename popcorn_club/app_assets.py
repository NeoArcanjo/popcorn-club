"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle
from popcorn_club.Auth.auth_assets import auth_bundles
from popcorn_club.Dashboard.dashboard_assets import dashboard_bundles
from popcorn_club.Main.main_assets import main_bundles
from popcorn_club.Spotify.spotify_assets import spotify_bundles

common_bundles = {
    "common_js": Bundle('src/js/*.js', 'src/vendor/*/*.js',
                        filters="jsmin",
                        output="dist/js/common.%(version)s.js"),
    "common_style": Bundle('src/css/*.css',
                           filters='cssmin',
                           output='dist/css/style.%(version)s.css')
}


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = True
    # "common_style": Bundle(
    #     'src/scss/*.scss',
    #     'src/scss/*/*.scss',
    #     filters='scss',
    #     output='dist/css/style.css',
    #     extra={'rel': 'stylesheet/scss'}
    # )

    # admin_style_bundle = Bundle(
    #     'admin_bp/scss/admin.scss',
    #     filters='pyscss,cssmin',
    #     output='dist/css/admin.css',
    #     extra={'rel': 'stylesheet/scss'}
    # )

    assets.register(common_bundles)
    # assets.register(admin_bundles)
    assets.register(auth_bundles)
    assets.register(dashboard_bundles)
    # assets.register(documentation_bundles)
    # assets.register(landing_bundles)
    assets.register(main_bundles)
    assets.register(spotify_bundles)

    if app.config['ENV'] == 'development':
        for app_bundle in [common_bundles, auth_bundles, dashboard_bundles, main_bundles, spotify_bundles]:
            for bundle in app_bundle.values():
                bundle.build()
    return assets
