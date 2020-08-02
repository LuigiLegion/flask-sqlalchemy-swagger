# Imports
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint
# from routes import request_api
# import json
# from pprint import pprint


# Constants
# Database file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'


# Initializations
# Initialize server
app = Flask(__name__)
# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASE_DIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize ORM
db = SQLAlchemy(app)
# Initialize serialization/deserialization
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


# Add schemas to APISpec
spec.components.schema("Product", schema=ProductSchema)
spec.components.schema("ProductId", schema=ProductParameter)


# Initialize Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'flask-sqlalchemy-swagger'
    }
)


# Register blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# app.register_blueprint(routes.request_api.get_blueprint())


# Routes
# Swagger UI
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Get all products
@app.route('/api/products', methods=['GET'])
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

    return jsonify(products), 200


# Get single product
@app.route('/api/products/<product_id>', methods=['GET'])
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

    return product_schema.jsonify(product), 200


# Create single product
@app.route('/api/products', methods=['POST'])
def create_product():
    """Single product POST view.
    ---
    post:
      requestBody:
        description: Product Object
        required: true
        content:
          application/json:
            schema: ProductSchema
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

    return product_schema.jsonify(product), 201


# Update single product
@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Single product PUT view.
    ---
    put:
      parameters:
      - in: path
        schema: ProductParameter
      requestBody:
        description: Product Object
        required: true
        content:
          application/json:
            schema: ProductSchema
      responses:
        202:
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

    return product_schema.jsonify(product), 202


# Delete single product
@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Single product DELETE view.
    ---
    delete:
      parameters:
      - in: path
        schema: ProductParameter
      responses:
        204:
          content:
            application/json:
              schema: ProductSchema
    """
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product), 204


# Register paths and entities within them
with app.test_request_context():
    spec.path(view=get_products)
    spec.path(view=get_product)
    spec.path(view=create_product)
    spec.path(view=update_product)
    spec.path(view=delete_product)


# Print APISpec to populate /static/swagger.json
# pprint(json.dumps(spec.to_dict()))


# Run server
if __name__ == '__main__':
    app.run(debug=True)
