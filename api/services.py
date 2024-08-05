import requests

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def fetch_books(query, max_results=10):
    params = {
        'q': query,
        'maxResults': max_results,
        'key': 'YOUR_API_KEY'  # Replace with your Google API key
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to fetch data from Google Books API'}
