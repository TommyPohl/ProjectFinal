from django.contrib import admin
from django.urls import path, include
from Bookshelf import views
from . import views
from .views import BookListView
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
]
