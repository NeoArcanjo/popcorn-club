"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    
    assets.auto_build = True
    assets.debug = False
    common_style_bundle = Bundle(
        'src/less/*.less',
        filters='less,cssmin',
        output='dist/css/style.css',
        extra={'rel': 'stylesheet/less'}
    )
    admin_style_bundle = Bundle(
        'admin_bp/less/admin.less',
        filters='less,cssmin',
        output='dist/css/admin.css',
        extra={'rel': 'stylesheet/less'}
    )
    auth_style_bundle = Bundle(
        'auth_bp/less/auth.less',
        filters='less,cssmin',
        output='dist/css/auth.css',
        extra={'rel': 'stylesheet/less'}
    )
    main_style_bundle = Bundle(
        'main_bp/less/main.less',
        filters='less,cssmin',
        output='dist/css/main.css',
        extra={'rel': 'stylesheet/less'}
    )
    dashboard_style_bundle = Bundle(
        'dashboard_bp/less/dashboard.less',
        filters='less,cssmin',
        output='dist/css/dashboard.css',
        extra={'rel': 'stylesheet/less'}
    )
    documentation_style_bundle = Bundle(
        'documentation_bp/less/documentation.less',
        filters='less,cssmin',
        output='dist/css/documentation.css',
        extra={'rel': 'stylesheet/less'}
    )
    landing_style_bundle = Bundle(
        'landing_bp/less/landing.less',
        filters='less,cssmin',
        output='dist/css/landing.css',
        extra={'rel': 'stylesheet/less'}
    )

    spotify_style_bundle = Bundle(
        'spotify_bp/less/spotify.less',
        filters='less,cssmin',
        output='dist/css/spotify.css',
        extra={'rel': 'stylesheet/less'}
    )

    assets.register('common_style_bundle', common_style_bundle)
    # assets.register('admin_style_bundle', admin_style_bundle)
    assets.register('auth_style_bundle', auth_style_bundle)
    assets.register('main_style_bundle', main_style_bundle)
    assets.register('dashboard_style_bundle', dashboard_style_bundle)
    # assets.register('documentation_style_bundle', documentation_style_bundle)
    # assets.register('landing_style_bundle', landing_style_bundle)
    assets.register('spotify_style_bundle', spotify_style_bundle)

    if app.config['FLASK_ENV'] == 'development':
        common_style_bundle.build()
        admin_style_bundle.build()
        auth_style_bundle.build()
        dashboard_style_bundle.build()
        documentation_style_bundle.build()
        landing_style_bundle.build()
        spotify_style_bundle.build()
    return assets


# {% assets "home_less_bundle" %}
#   <link
#     href="{{ ASSET_URL }}"
#     rel="stylesheet"
#     type="text/css"
#   />
# {% endassets %}