from django.contrib import admin
from django.urls import path, include

from Bookshelf.views.books import (
    BookListView, book_detail, add_book, import_books,
    BookUpdateView, BookDeleteView, toggle_read, toggle_wishlist,
    export_books, read_books_view, my_library,
    ReadBooksListView, WishlistBooksListView,
    BestRatedBooksView, WorstRatedBooksView, wishlist_view
)
from Bookshelf import views
from Bookshelf.views.users import register, home
from Bookshelf.views.static_pages import about, reading_room
from Bookshelf.views.authors import author_list, books_by_author
from Bookshelf.views.genres import genre_list, genre_detail
from Bookshelf.views.tags import create_tag, tag_list, tag_detail, edit_tag, delete_tag
from Bookshelf.views.loans import loans_view
from Bookshelf.views import loans

from Bookshelf.views._404 import custom_404_view

handler404 = 'Bookshelf.views._404.custom_404_view'

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('admin/', admin.site.urls),

    # Books
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/add/', add_book, name='add-book'),
    path('books/import/', import_books, name='import-books'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book-edit'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/toggle-read/', toggle_read, name='toggle-read'),
    path('books/<int:pk>/toggle-wishlist/', toggle_wishlist, name='toggle-wishlist'),
    path('books/read/', ReadBooksListView.as_view(), name='books-read'),
    path('books/wishlist/', WishlistBooksListView.as_view(), name='books-wishlist'),
    path('books/best-rated/', BestRatedBooksView.as_view(), name='books-best-rated'),
    path('books/worst-rated/', WorstRatedBooksView.as_view(), name='books-worst-rated'),
    path('books/export/', export_books, name='export-books'),

    # Authors
    path('autori/', author_list, name='authors-list'),
    path('authors/<str:author_name>/', books_by_author, name='books-by-author'),

    # Genres
    path('zanry/', genre_list, name='genres'),
    path('genres/<str:genre>/', genre_detail, name='genre-detail'),
    path('zanr/<str:genre>/', views.books_by_genre, name='genre-detail'),

    # Tags
    path('tags/create/', create_tag, name='create-tag'),
    path('stitky/', tag_list, name='tag-list'),
    path('stitky/<str:slug>/', tag_detail, name='tag-detail'),
    path('tags/<str:slug>/edit/', edit_tag, name='edit-tag'),
    path('tags/<str:slug>/delete/', delete_tag, name='delete-tag'),

    # Static Pages
    path('about/', about, name='about'),
    path('reading-room/', reading_room, name='reading-room'),

    # User-specific views
    path('wishlist/', wishlist_view, name='books-wishlist'),
    path('read/', read_books_view, name='books-read'),
    path('moje-knihovna/', my_library, name='my-library'),

    # Loans
    path('vypujcky/', loans_view, name='loans'),
]
