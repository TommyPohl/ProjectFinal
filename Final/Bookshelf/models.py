from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    series = models.CharField(max_length=100, blank=True)
    published_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=20, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="books")

    def __str__(self):
        return self.title

class UserBookRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    wishlist = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} – {self.book.title}: {self.stars}★"

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



