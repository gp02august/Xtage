from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField()
    rating = models.FloatField()

    def _str_(self):
        return self.title

class Recommendation(models.Model):
    book = models.ForeignKey(Book, related_name='recommendations', on_delete=models.CASCADE)
    recommended_book = models.CharField(max_length=200)

    def _str_(self):
        return self.recommended_book

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='likes', on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)