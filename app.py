# Imports
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Constants
# Database file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Initializations
# Initialize server
app = Flask(__name__)
# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
db = SQLAlchemy(app)
# Initialize serialization
ma = Marshmallow(app)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
