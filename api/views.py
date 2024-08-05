from rest_framework import viewsets, generics
from django.shortcuts import render, redirect
from .models import Book, Recommendation
from .serializers import BookSerializer, RecommendationSerializer
import requests

class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q=python')
        if response.status_code == 200:
            books = response.json().get('items', [])
            for book in books:
                volume_info = book.get('volumeInfo', {})
                book_data = {
                    'title': volume_info.get('title', ''),
                    'author': ', '.join(volume_info.get('authors', [])),
                    'description': volume_info.get('description', ''),
                    'cover_image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'rating': volume_info.get('averageRating', 0)
                }
                Book.objects.create(**book_data)
        serializer.save()

class RecommendationListCreate(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        recommended_books = generate_recommendations(book)  # Implement this function to generate recommendations
        for recommended_book_title in recommended_books:
            Recommendation.objects.create(book=book, recommended_book=recommended_book_title)
        serializer.save()

def generate_recommendations(book):
    # Find books with the same author
    recommendations = Book.objects.filter(author=book.author).exclude(id=book.id)
    recommended_titles = [rec_book.title for rec_book in recommendations]
    
    # If not enough recommendations, add books with similar titles
    if len(recommended_titles) < 3:
        similar_title_books = Book.objects.filter(title__icontains=book.title.split()[0]).exclude(id=book.id)
        for rec_book in similar_title_books:
            if rec_book.title not in recommended_titles:
                recommended_titles.append(rec_book.title)
                if len(recommended_titles) >= 3:
                    break

    return recommended_titles[:3]  # Return up to 3 recommendations

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'api/book_list.html', {'books': books})

def redirect_to_book_list(request):
    return redirect('book-list')

def welcome(request):
    return render(request, 'api/welcome.html')

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer