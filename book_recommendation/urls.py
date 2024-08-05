from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import book_list, redirect_to_book_list, welcome  # Import the welcome view

schema_view = get_schema_view(
    openapi.Info(
        title="Book Recommendation API",
        default_version='v1',
        description="API documentation for the Book Recommendation project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@book.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome, name='welcome'),  # Set the welcome view as the root URL
    path('api/', include('api.urls')),  # Include the API URLs
    path('book-list/', book_list, name='book-list'),  # Handle the book-list URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]