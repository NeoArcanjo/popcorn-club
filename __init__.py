def create_app():
    from flask import Flask
    # App config
    app = Flask(__name__)
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
