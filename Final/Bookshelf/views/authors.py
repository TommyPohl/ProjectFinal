from django.shortcuts import render
from django.db.models import Count
from django.db.models import Avg
from django.db.models.functions import Lower

from Bookshelf.models import Book


def author_list(request):
    # Získání hodnoty hledání z URL parametru
    search_query = request.GET.get('search', '')

    if search_query:
        # Pokud je zadán text pro hledání, filtrovat autory podle jména
        authors = Book.objects.exclude(author='') \
            .filter(author__icontains=search_query) \
            .values('author') \
            .annotate(book_count=Count('id')) \
            .order_by(Lower('author'))
    else:
        # Pokud není zadán hledaný text, zobrazíme všechny autory
        authors = Book.objects.exclude(author='') \
            .values('author') \
            .annotate(book_count=Count('id')) \
            .order_by(Lower('author'))

    return render(request, 'authors/author_list.html', {'authors': authors, 'search_query': search_query})

def books_by_author(request, author_name):
    books = Book.objects.filter(author=author_name).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'authors/books_by_author.html', {'books': books, 'author_name': author_name})
