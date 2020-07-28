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


# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(250))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# Initialize schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Routes
# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products_raw = Product.query.all()
    products = products_schema.dump(products_raw)

    return jsonify(products)


# Get single product
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)

    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
