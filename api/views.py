from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Book, Recommendation, Like, Comment
from .serializers import BookSerializer, RecommendationSerializer, LikeSerializer, CommentSerializer
import requests

class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class RecommendationListCreate(generics.ListCreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        recommended_books = generate_recommendations(book)
        for recommended_book_title in recommended_books:
            Recommendation.objects.create(book=book, recommended_book=recommended_book_title)
        serializer.save()

class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class CommentListCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

def generate_recommendations(book):
    recommendations = Book.objects.filter(author=book.author).exclude(id=book.id)
    recommended_titles = [rec_book.title for rec_book in recommendations]
    if len(recommended_titles) < 3:
        similar_title_books = Book.objects.filter(title__icontains=book.title.split()[0]).exclude(id=book.id)
        for rec_book in similar_title_books:
            if rec_book.title not in recommended_titles:
                recommended_titles.append(rec_book.title)
                if len(recommended_titles) >= 3:
                    break
    return recommended_titles[:3]

# def book_list(request):
#     query = request.GET.get('q')
#     if query:
#         books = Book.objects.filter(title__icontains=query)
#     else:
#         books = Book.objects.all()

#     # Check if it's an API request
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/'):
#         serializer = BookSerializer(books, many=True)
#         return JsonResponse(serializer.data, safe=False)  # Return JSON response for API requests

#     # Otherwise, render HTML
#     return render(request, 'api/book_list.html', {'books': books})

def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/'):
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
    
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

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer