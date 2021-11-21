"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle

main_style_bundle = Bundle(
    'main_bp/src/css/*.css',
    filters='cssmin',
    output='dist/css/main.css'
)
# admin_style_bundle = Bundle(
#     'admin_bp/less/admin.less',
#     filters='pyscss,cssmin',
#     output='dist/css/admin.css',
#     extra={'rel': 'stylesheet/less'}
# )
# auth_style_bundle = Bundle(
#     'auth_bp/less/auth.less',
#     filters='pyscss,cssmin',
#     output='dist/css/auth.css',
#     extra={'rel': 'stylesheet/less'}
# )

# dashboard_style_bundle = Bundle(
#     'dashboard_bp/scss/*.scss',
#     'dashboard_bp/scss/*/*.scss',
#     filters='pyscss,cssmin',
#     output='dist/css/dashboard.css',
#     extra={'rel': 'stylesheet/scss'}
# )
# documentation_style_bundle = Bundle(
#     'documentation_bp/less/documentation.less',
#     filters='pyscss,cssmin',
#     output='dist/css/documentation.css',
#     extra={'rel': 'stylesheet/less'}
# )
# landing_style_bundle = Bundle(
#     'landing_bp/less/landing.less',
#     filters='pyscss,cssmin',
#     output='dist/css/landing.css',
#     extra={'rel': 'stylesheet/less'}
# )

# spotify_style_bundle = Bundle(
#     'spotify_bp/less/spotify.less',
#     filters='pyscss,cssmin',
#     output='dist/css/spotify.css',
#     extra={'rel': 'stylesheet/less'}
# )

    


# {% assets "home_less_bundle" %}
#   <link
#     href="{{ ASSET_URL }}"
#     rel="stylesheet"
#     type="text/css"
#   />
# {% endassets %}
