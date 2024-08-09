from flask import Flask
from app.routes import main_routes

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(main_routes)

    return app
