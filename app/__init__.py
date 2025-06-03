from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# Correct path for site.db in the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_root, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key' # It's good practice to set this

db = SQLAlchemy(app)

# Import routes and models after db initialization to avoid circular imports
from app import routes, models

# If you have any CLI commands or context processors, they can be initialized here too.
