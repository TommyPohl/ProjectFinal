from django.shortcuts import render
from django.db.models import Count, Avg
from ..models import Book
from django.db.models import Q

def genre_list(request):
    genres = Book.objects.values('genre').annotate(count=Count('id')).order_by('genre')
    return render(request, 'genres/genre_list.html', {'genres': genres})

def genre_detail(request, genre):
    books = Book.objects.filter(genre=genre).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'genres/genre_detail.html', {'genre': genre, 'books': books})

def books_by_genre(request, genre):
    books = Book.objects.filter(genre=genre)
    return render(request, 'books/book_list_by_genre.html', {
        'genre': genre,
        'books': books
    })
