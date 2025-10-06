from flask import Flask
from flask_scss import Scss
from .models import db
from .routes import main

def create_app():
    app = Flask(__name__)
    Scss(app)   

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
    
    return app