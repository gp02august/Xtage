# book_recommendation/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Welcome to the Book Recommendation System</h1><p>Visit <a href='/api/book-list/'>Book List</a> to see the books.</p>")
