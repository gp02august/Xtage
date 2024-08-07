from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RecommendationViewSet, LikeViewSet, CommentViewSet, book_list, welcome

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/', book_list, name='book_list'),
    path('book-list/', book_list, name='book-list'),
    path('welcome/', welcome, name='welcome'),
]