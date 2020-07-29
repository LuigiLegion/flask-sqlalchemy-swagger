# Imports
import os
import json
from pprint import pprint
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin


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


# Product schemas
class ProductSchema(ma.Schema):
    id = ma.Integer()
    name = ma.String()
    description = ma.String()
    price = ma.Integer()
    quantity = ma.Integer()

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


class ProductParameter(ma.Schema):
    product_id = ma.Integer()


# Initialize schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Initialize APISpec
spec = APISpec(
    title="flask-sqlalchemy-swagger",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="A minimal product catalogue management API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


# Add schema to APISpec
spec.components.schema("Product", schema=ProductSchema)


# Routes
# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    """Single product GET view.
    ---
    get:
      responses:
        200:
          content:
            application/json:
              schema: ProductSchema
    """
    products_raw = Product.query.all()
    products = products_schema.dump(products_raw)

    return jsonify(products)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=get_products)


# Get single product
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Single product GET view.
    ---
    get:
      parameters:
      - in: path
        schema: ProductParameter
      responses:
        200:
          content:
            application/json:
              schema: ProductSchema
    """
    product = Product.query.get(product_id)

    return product_schema.jsonify(product)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=get_product)


# Create single product
@app.route('/products', methods=['POST'])
def create_product():
    """Single product POST view.
    ---
    post:
      responses:
        201:
          content:
            application/json:
              schema: ProductSchema
    """
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product = Product(name, description, price, quantity)

    db.session.add(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=create_product)


# Update single product
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Single product PUT view.
    ---
    put:
      parameters:
      - in: path
        schema: ProductParameter
      responses:
        200:
          content:
            application/json:
              schema: ProductSchema
    """
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product = Product.query.get(product_id)

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=update_product)


# Delete single product
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Single product DELETE view.
    ---
    delete:
      parameters:
      - in: path
        schema: ProductParameter
      responses:
        200:
          content:
            application/json:
              schema: ProductSchema
    """
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=delete_product)


# Print OpenAPI spec
# pprint(json.dumps(spec.to_dict()))


# Run server
if __name__ == '__main__':
    app.run(debug=True)
