"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle

app.register_blueprint(auth.bp)
app.register_blueprint(club.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(spotify.spotify_bp)
def compile_static_assets(assets):
    """Configure and build asset bundles."""

    # Main asset bundles
    auth_style_bundle = Bundle(
        'static/scss/*.scss',
        'bp/homepage.less',
        filters='less,cssmin',
        output='dist/css/landing.css',
        extra={'rel': 'stylesheet/css'}
    )
    main_js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js'
    )

    # Admin asset bundleds
    admin_style_bundle = Bundle(
        'src/less/*.less',
        'admin_bp/admin.less',
        filters='less,cssmin',
        output='dist/css/account.css',
        extra={'rel': 'stylesheet/css'}
    )
    assets.register('main_styles', main_style_bundle)
    assets.register('main_js', main_js_bundle)
    assets.register('admin_styles', admin_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        main_style_bundle.build()
        main_js_bundle.build()
        admin_style_bundle.build()
