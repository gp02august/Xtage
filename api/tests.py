from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Book, Recommendation, Like, Comment
from .serializers import BookSerializer, RecommendationSerializer, LikeSerializer, CommentSerializer

class BookModelTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            cover_image='http://example.com/cover.jpg',
            rating=4.5
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.description, 'Test Description')
        self.assertEqual(self.book.cover_image, 'http://example.com/cover.jpg')
        self.assertEqual(self.book.rating, 4.5)

class RecommendationModelTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            cover_image='http://example.com/cover.jpg',
            rating=4.5
        )
        self.recommendation = Recommendation.objects.create(
            book=self.book,
            recommended_book='Another Recommended Book'
        )

    def test_recommendation_creation(self):
        self.assertEqual(self.recommendation.book.title, 'Test Book')
        self.assertEqual(self.recommendation.recommended_book, 'Another Recommended Book')

class LikeModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            cover_image='http://example.com/cover.jpg',
            rating=4.5
        )
        self.like = Like.objects.create(
            user=self.user,
            book=self.book
        )

    def test_like_creation(self):
        self.assertEqual(self.like.book.title, 'Test Book')
        self.assertEqual(self.like.user.username, 'testuser')

class CommentModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            cover_image='http://example.com/cover.jpg',
            rating=4.5
        )
        self.comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            text='This is a comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.book.title, 'Test Book')
        self.assertEqual(self.comment.text, 'This is a comment')
        self.assertEqual(self.comment.user.username, 'testuser')

class BookAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            'title': 'API Test Book',
            'author': 'API Test Author',
            'description': 'API Test Description',
            'cover_image': 'http://example.com/api_cover.jpg',
            'rating': 5.0
        }
        self.book = Book.objects.create(**self.book_data)
        self.valid_payload = {
            'title': 'API Test Book 2',
            'author': 'API Test Author 2',
            'description': 'API Test Description 2',
            'cover_image': 'http://example.com/api_cover2.jpg',
            'rating': 4.0
        }

    def test_get_all_books(self):
        response = self.client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)  # Use response.json() instead of response.data

    def test_create_book(self):
        response = self.client.post(reverse('book-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'API Test Book 2')

class RecommendationAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title='Rec Test Book',
            author='Rec Test Author',
            description='Rec Test Description',
            cover_image='http://example.com/rec_cover.jpg',
            rating=3.5
        )
        self.recommendation_data = {
            'book': self.book.id,
            'recommended_book': 'Another Recommended Book'
        }

    def test_create_recommendation(self):
        response = self.client.post(reverse('recommendation-list'), data=self.recommendation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recommendation.objects.count(), 1)
        self.assertEqual(Recommendation.objects.get(id=1).recommended_book, 'Another Recommended Book')

class LikeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Like Test Book',
            author='Like Test Author',
            description='Like Test Description',
            cover_image='http://example.com/like_cover.jpg',
            rating=4.5
        )
        self.like_data = {
            'user': self.user.id,
            'book': self.book.id
        }

    def test_create_like(self):
        response = self.client.post(reverse('like-list'), data=self.like_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get(id=1).book.title, 'Like Test Book')
        self.assertEqual(Like.objects.get(id=1).user.username, 'testuser')

class CommentAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Comment Test Book',
            author='Comment Test Author',
            description='Comment Test Description',
            cover_image='http://example.com/comment_cover.jpg',
            rating=4.5
        )
        self.comment_data = {
            'user': self.user.id,
            'book': self.book.id,
            'text': 'This is a comment'
        }

    def test_create_comment(self):
        response = self.client.post(reverse('comment-list'), data=self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get(id=1).book.title, 'Comment Test Book')
        self.assertEqual(Comment.objects.get(id=1).text, 'This is a comment')
        self.assertEqual(Comment.objects.get(id=1).user.username, 'testuser')