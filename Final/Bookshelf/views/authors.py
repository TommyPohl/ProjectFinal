from django.shortcuts import render
from django.db.models import Count
from django.db.models import Avg

from Bookshelf.models import Book


def author_list(request):
    authors = Book.objects.values('author').annotate(book_count=Count('id')).order_by('author')
    return render(request, 'authors/author_list.html', {'authors': authors})

def books_by_author(request, author_name):
    books = Book.objects.filter(author=author_name).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'authors/books_by_author.html', {'books': books, 'author_name': author_name})
