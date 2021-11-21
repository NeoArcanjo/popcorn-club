"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle
from popcorn_club.Auth.auth_assets import auth_style_bundle
from popcorn_club.Dashboard.dashboard_assets import dashboard_style_bundle
from popcorn_club.Main.main_assets import main_style_bundle
from popcorn_club.Spotify.spotify_assets import spotify_style_bundle

def compile_static_assets(assets):
    """Create stylesheet bundles."""
    
    assets.auto_build = True
    assets.debug = True
    # common_style_bundle = Bundle(
    #     'src/scss/*.scss',
    #     'src/scss/*/*.scss',
    #     filters='scss',
    #     output='dist/css/style.css',
    #     extra={'rel': 'stylesheet/scss'}
    # )
    common_style_bundle = Bundle(
        'src/css/*.css',
        filters='cssmin',
        output='dist/css/style.css'
    )
    # admin_style_bundle = Bundle(
    #     'admin_bp/scss/admin.scss',
    #     filters='pyscss,cssmin',
    #     output='dist/css/admin.css',
    #     extra={'rel': 'stylesheet/scss'}
    # )
    
    assets.register('common_style_bundle', common_style_bundle)
    # # assets.register('admin_style_bundle', admin_style_bundle)
    assets.register('auth_style_bundle', auth_style_bundle)
    assets.register('main_style_bundle', main_style_bundle)
    assets.register('dashboard_style_bundle', dashboard_style_bundle)
    # # assets.register('documentation_style_bundle', documentation_style_bundle)
    # # assets.register('landing_style_bundle', landing_style_bundle)
    assets.register('spotify_style_bundle', spotify_style_bundle)

    if app.config['FLASK_ENV'] == 'development':
        common_style_bundle.build()
        # admin_style_bundle.build()
        auth_style_bundle.build()
        dashboard_style_bundle.build()
        # documentation_style_bundle.build()
        # landing_style_bundle.build()
        main_style_bundle.build()
        spotify_style_bundle.build()
    return assets


# {% assets "home_less_bundle" %}
#   <link
#     href="{{ ASSET_URL }}"
#     rel="stylesheet"
#     type="text/css"
#   />
# {% endassets %}