# Flask-SQLAlchemy-Swagger

## Dev Environment Setup:

```bash
# Initialize virtual environment
$ pipenv shell

# Install dependencies
$ pipenv install

# Create database
$ python3
>> from app import db
>> db.create_all()
>> exit()

# Run server (http://localhost:5000)
python3 app.py
```

## Swagger UI:

Navigate to generated Swagger UI in your browser of choice at http://localhost:5000/swagger

## REST API Endpoints:

- GET /products
- GET /products/:product_id
- POST /products
- PUT /products/:product_id
- DELETE /products/:product_id
