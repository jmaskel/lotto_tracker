from flask import Flask
from .views import main_blueprint

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app
