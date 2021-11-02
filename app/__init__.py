from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os 

db = SQLAlchemy() # acts as our connection point to database
migrate = Migrate() # used for when we make changes to our models to keep things up-to-date
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # DB Configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # b/c we don't want SQLAlchemy to track
    
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    # Import models here 
    from app.models.book import Book 
    
    db.init_app(app)
    migrate.init_app(app, db) # connects DB and migrates to Flask app, using Migrate package's syntax

    # Register blueprints here 
    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app
