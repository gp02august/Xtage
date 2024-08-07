# Book Recommendation API

This project provides an API for book recommendations. It includes functionalities for managing books, recommendations, likes, and comments. The project is built using Django and Django REST framework.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.6+
- Django 3.1+
- Django REST framework

### Steps

1. Clone the repository:
   bash
   git clone https://github.com/gp02august/book_recommendation.git
   cd book_recommendation
2. Create a virtual environment:
   bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
3. Install the required packages:
   bash
   pip install -r requirements.txt
4. Set up the database:
   bash
   python manage.py migrate

## Configuration

1. Create a .env file in the root directory and add the following environment variables:
   env
   SECRET_KEY=your_secret_key
   DEBUG=True
2. Update settings.py to read these environment variables.

## Running the Server

1. Start the Django development server:
   bash
   python manage.py runserver
2. Open your web browser and navigate to:

   - Welcome Page: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Book List: [http://127.0.0.1:8000/book-list/](http://127.0.0.1:8000/book-list/)
   - API Documentation (Swagger): [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
   - API Documentation (Redoc): [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Testing

1. Run the test suite to ensure everything is working correctly:
   bash
   python manage.py test

## API Endpoints

The following endpoints are available in the API:

- /api/books/ (GET, POST): List all books or create a new book
- /api/recommendations/ (GET, POST): List all recommendations or create a new recommendation
- /api/likes/ (GET, POST): List all likes or create a new like
- /api/comments/ (GET, POST): List all comments or create a new comment

## Frontend

The project includes a simple frontend to display the book list and search functionality.

### Templates

- index.html: The main page to display the list of books.
- welcome.html: The welcome page.

### AJAX Integration

The project uses AJAX to fetch and display book data without refreshing the page.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature/your-feature).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Created by [gp02august](https://github.com/gp02august).
