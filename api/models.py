from django.db import models

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