"""Compile static assets."""
from flask_assets import Bundle

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

bundles = {
    "common_js": Bundle('src/js/*.js', 'src/vendor/*/*.js',
                        filters="jsmin",
                        output="dist/js/common.%(version)s.js"),
    "common_style": Bundle('src/css/*.css',
                           filters='cssmin',
                           output='dist/css/style.%(version)s.css'),
    "admin_js": Bundle('admin_bp/src/js/*.js',
                       filters="jsmin",
                       output="dist/js/admin.%(version)s.js"),
    "admin_style": Bundle('admin_bp/src/css/*.css',
                          filters='cssmin',
                          output='dist/css/admin.%(version)s.css'),
                          "auth_js": Bundle('auth_bp/src/js/*.js',
                      filters="jsmin",
                      output="dist/js/auth.%(version)s.js"),
    "auth_style": Bundle('auth_bp/src/css/*.css',
                         filters='cssmin',
                         output='dist/css/auth.%(version)s.css'),
                         "dashboard_js": Bundle('dashboard_bp/src/js/*.js', 'dashboard_bp/src/vendor/*/*.js',
                           filters="jsmin",
                           output="dist/js/dashboard.%(version)s.js"),
    "dashboard_style": Bundle('dashboard_bp/src/css/*.css',
                              filters='cssmin',
                              output='dist/css/dashboard.%(version)s.css'),
                              "documentation_js": Bundle('documentation_bp/src/js/*.js',
                               filters="jsmin",
                               output="dist/js/documentation.%(version)s.js"),
    "documentation_style": Bundle('documentation_bp/src/css/*.css',
                                  filters='cssmin',
                                  output='dist/css/documentation.%(version)s.css'),
                                  "landing_js": Bundle('landing_bp/src/js/*.js',
                         filters="jsmin",
                         output="dist/js/landing.%(version)s.js"),
    "landing_style": Bundle('landing_bp/src/css/*.css',
                            filters='cssmin',
                            output='dist/css/landing.%(version)s.css'),
                            "main_js": Bundle('main_bp/src/js/*.js',
                      filters="jsmin",
                      output="dist/js/main.%(version)s.js"),
    "main_style": Bundle('main_bp/src/css/*.css',
                         filters='cssmin',
                         output='dist/css/main.%(version)s.css'),
                         "spotify_js": Bundle('spotify_bp/src/js/*.js',
                         filters="jsmin",
                         output="dist/js/spotify.%(version)s.js"),
    "spotify_style": Bundle('spotify_bp/src/css/*.css',
                            filters='cssmin',
                            output='dist/css/spotify.%(version)s.css'),
                            "test_scss": Bundle('spotify_bp/src/scss/*.scss', filters='pyscss',
       output='dist/css/spotify.%(version)s.css')
}