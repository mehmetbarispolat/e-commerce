# E-Commerce API with Django & Django REST Framework

This project is a simple e-commerce API developed with Django and Django REST Framework.

## Features

- Product management (add, update, delete)
- Stock management for products
- Bundle products, which group together individual products
- Sales channels to sell products

## TODO List

Here's a list of tasks and enhancements planned for future development of this E-Commerce project:

- [ ] Optimize the query performance for fetching products, especially Bundle products with many items (use `select_related`).
- [ ] Changed the project folder structure by Domain Driven Desing. For example: 
    ```
        /src/product/ - Product App
        /src/order/ - Order App
        /src/user/ - User App
        /tests/src/product/ - For product tests.
    ```
- [ ] Implement Celery tasks to periodically fetch products, etc. from Sales Channels.
- [ ] Implement a caching mechanism to improve response times for frequently accessed data.
- [ ] Add Stock List and Price List to add into a Catalog for each Sales Channel. Stock and Price Management would be more easier.
- [ ] Add user authentication and authorization for managing products and sales channels.
- [ ] Develop a more comprehensive testing strategy, including unit and integration tests, to ensure reliability.
- [ ] Integrate with an external payment gateway for processing transactions.
- [ ] Implement a recommendation engine to suggest products to users based on their browsing history.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Docker (Optional. You can work on your local environment. If you want this, skip the development container section.) 

### Development Container
This project includes support for VSCode's Development Containers. To use it, ensure you have Docker installed, and the Dev Containers extension enabled in VSCode.

Open the project folder in VSCode, and when prompted, choose to reopen in a container. This will build the Docker image and start a container with all the necessary development tools pre-installed.

You can click [here](https://code.visualstudio.com/docs/devcontainers/containers) for more information.

### Installing

First, clone the repository to your local machine:

```bash
git clone https://github.com/mehmetbarispolat/e-commerce.git
cd e-commerce
```

Create a network named `ecommercenet`(in .devcontainer.json) on Docker.

```bash
docker network create ecommercenet
```

Use CTRL(Cmd for MacOS)+ Shift + P to run a container in the project folder.

```
>Dev Containers: Open Folder in Container
```

Then, create a virtual environment to isolate our package dependencies locally:

```bash
python -m venv .venv
# On Windows use `python -m venv venv`
```

Activate the virtual environment:

```bash
source .venv/bin/activate
# On Windows use `.\venv\Scripts\activate`
```

Install the project dependencies:

```bash
pip install -e .[dev]
```

### Setting Up the Database

Run the following command to create the necessary database tables:

```bash
python manage.py migrate
```

### Running the Development Server

To start the development server, use the following command:

```bash
python manage.py runserver
```

Now, the API should be accessible at `http://127.0.0.1:8000/api/v1/`.

### API Endpoints

- `GET /api/v1/products/`: List all products.
- `POST /api/v1/products/`: Create a new product.
- `GET /api/v1/products/<pk>/`: Retrieve a specific product.
- `PUT /api/v1/products/<pk>/`: Update a specific product.
- `DELETE /api/v1/products/<pk>/`: Delete a specific product.

## Running Tests

To run tests, execute:

```bash
python manage.py test
```

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django REST Framework](https://www.django-rest-framework.org/) - The framework used for creating the API

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/mehmetbarispolat/e-commerce/LICENSE.md) file for details
```