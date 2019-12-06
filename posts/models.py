from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    draft = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField()

    def __str__(self):
        return f"Post: {self.title} ({self.created.strftime('%Y-%m-%d %H:%M')})"
