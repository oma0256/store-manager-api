[![Build Status](https://travis-ci.org/oma0256/store-manager-api.svg?branch=challenge3)](https://travis-ci.org/oma0256/store-manager-api)
<!-- [![Coverage Status](https://coveralls.io/repos/github/oma0256/store-manager-api/badge.svg?branch=challenge3)](https://coveralls.io/github/oma0256/store-manager-api?branch=challenge3) -->
[![Maintainability](https://api.codeclimate.com/v1/badges/3303ae1c369c0bd693df/maintainability)](https://codeclimate.com/github/oma0256/store-manager-api/maintainability)
# Store Manager Api
Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

## Getting Started
To get the application up and running on your computer you can run ```git clone https://github.com/oma0256/store-manager.git```.

### Prerequisites
You have to have python 3.6 and pip installed on your computer.

### Installing
Navigate to where you cloned the repository
- ```cd store-manager-api```
- ```virtual venv```
- ```cd venv```
- ```./Scripts/activate```
- ```pip install -r requirements.txt```

## Running the tests
To run the test
- ```cd store-manager-api```
- ```python -m pytest```

## Features
The store owner can perform the following tasks:
- Register a store attendant
- Add a new product
- View all products
- View an individual product
- View all sale records
- View an individual sale record

The store attendant can perform the following tasks:
- Create a sale record
- View a single sale record if they created it
- View all products
- View an individual product

## Endpoints
HTTP Method | End point | Action
-----------|-----------|----------
POST | api/v2/auth/login | Login a user
POST | api/v2/auth/signup | Register a store attendant
POST | api/v2/sales | Create a sales record
GET | api/v2/sales | Retrieve all sales record
GET | api/v2/sales/sale_id | Retrieve a single sale record
POST | api/v2/products | Add a product
GET | api/v2/products | Retrieve all products
GET | api/v2/products/product_id | Retrieve a single product
PUT | api/v2/products/product_id | Modify a single product
DELETE | api/v2/products/product_id | Delete a single product
POST | api/v2/categories | Create a category
PUT | api/v2/categories/category_id | Modify a single category
DELETE | api/v2/categories/category_id | Delete a single category

## Built With
- Flask python's web framework

## Author
[Jonathan Omarwoth](https://github.com/oma0256)
