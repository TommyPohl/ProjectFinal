from django.contrib import admin
from django.urls import path, include
from Bookshelf import views
from . import views
from .views import BookListView
from .views import author_list
from .views import (
    ReadBooksListView, WishlistBooksListView,
    BestRatedBooksView, WorstRatedBooksView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),  # přidat tento řádek
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/add/', views.add_book, name='add-book'),
    path('books/import/', views.import_books, name='import-books'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book-edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/toggle-read/', views.toggle_read, name='toggle-read'),
    path('books/<int:pk>/toggle-wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('books/read/', ReadBooksListView.as_view(), name='books-read'),
    path('books/wishlist/', WishlistBooksListView.as_view(), name='books-wishlist'),
    path('books/best-rated/', BestRatedBooksView.as_view(), name='books-best-rated'),
    path('books/worst-rated/', WorstRatedBooksView.as_view(), name='books-worst-rated'),
    path('books/export/', views.export_books, name='export-books'),
    path('about/', views.about, name='about'),
    path('loans/', views.loans, name='loans'),
    path('reading-room/', views.reading_room, name='reading-room'),
    path('autori/', views.author_list, name='authors-list'),
    path('zanry/', views.genre_list, name='genres'),
    path('wishlist/', views.wishlist_view, name='books-wishlist'),
    path('read/', views.read_books_view, name='books-read'),
    path('moje-knihovna/', views.my_library, name='my-library'),
    path('authors/<str:author_name>/', views.books_by_author, name='books-by-author'),
    path('genres/<str:genre>/', views.genre_detail, name='genre-detail'),
]
