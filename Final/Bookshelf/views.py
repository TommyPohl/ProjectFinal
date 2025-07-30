from django.views.generic import ListView
from .models import Book, UserBookRelation
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import BookForm
import csv
from io import TextIOWrapper
from django.contrib import messages
from .forms import ImportBooksForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Rating
from .forms import RatingForm
from django.db import models
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Subquery, OuterRef
from django.db.models import Q
from django.http import HttpResponse
from .models import Author
from django.contrib.auth.decorators import login_required
from django.db.models import Count

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.annotate(avg_rating=Avg('rating__stars'))

        q = self.request.GET.get('q')
        author = self.request.GET.get('author')
        genre = self.request.GET.get('genre')
        series = self.request.GET.get('series')
        location = self.request.GET.get('location')
        sort_by = self.request.GET.get('sort')

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(author__icontains=q))
        if author:
            queryset = queryset.filter(author__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if series:
            queryset = queryset.filter(series__icontains=series)
        if location:
            queryset = queryset.filter(location__icontains=location)

        if sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'title_desc':
            queryset = queryset.order_by('-title')
        elif sort_by == 'author':
            queryset = queryset.order_by('author')
        elif sort_by == 'author_desc':
            queryset = queryset.order_by('-author')
        elif sort_by == 'genre':
            queryset = queryset.order_by('genre')
        elif sort_by == 'genre_desc':
            queryset = queryset.order_by('-genre')
        elif sort_by == 'location':
            queryset = queryset.order_by('location')
        elif sort_by == 'location_desc':
            queryset = queryset.order_by('-location')
        elif sort_by == 'published':
            queryset = queryset.order_by('-published_date')
        elif sort_by == 'published_desc':
            queryset = queryset.order_by('published_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['sort_by'] = self.request.GET.get('sort', '')  # ← DŮLEŽITÉ!
        context['filters'] = {
            'author': self.request.GET.get('author', ''),
            'genre': self.request.GET.get('genre', ''),
            'series': self.request.GET.get('series', ''),
            'location': self.request.GET.get('location', ''),
        }
        return context

def home(request):
    context = {}  # 💡 tady to přidáme hned na začátku

    recently_rated = Rating.objects.select_related('book', 'user')[:5]
    recent_comments = Rating.objects.exclude(comment='').select_related('book', 'user')[:5]
    newest_books = Book.objects.annotate(avg_rating=Avg('rating__stars')).order_by('-id')[:5]

    context.update({
        'recently_rated': recently_rated,
        'recent_comments': recent_comments,
        'newest_books': newest_books,
    })

    if request.user.is_authenticated:
        relations = UserBookRelation.objects.filter(user=request.user)

        recently_read_ids = relations.filter(read=True).values_list('book_id', flat=True)
        to_read_ids = relations.filter(wishlist=True).values_list('book_id', flat=True)

        recently_read = Book.objects.filter(id__in=recently_read_ids).annotate(avg_rating=Avg('rating__stars'))
        to_read = Book.objects.filter(id__in=to_read_ids).annotate(avg_rating=Avg('rating__stars'))

        # ⚠️ Osobní hodnocení (z přečtených knih uživatele)
        user_ratings = Rating.objects.filter(user=request.user, book=OuterRef('pk')).values('stars')[:1]
        recently_read = recently_read.annotate(user_stars=Subquery(user_ratings))

        best_rated_books = recently_read.exclude(user_stars__isnull=True).order_by('-user_stars')[:5]
        worst_rated_books = recently_read.exclude(user_stars__isnull=True).order_by('user_stars')[:5]

        context.update({
            'recently_read': recently_read,
            'to_read': to_read,
            'best_rated_books': best_rated_books,
            'worst_rated_books': worst_rated_books,
        })
    else:
        # 🌍 Globální hodnocení pro nepřihlášené
        best_rated_books = Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        worst_rated_books = Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('avg_rating')[:5]

        context.update({
            'best_rated_books': best_rated_books,
            'worst_rated_books': worst_rated_books,
        })

    return render(request, 'home_authenticated.html' if request.user.is_authenticated else 'home.html', context)

    context = {
        'recently_rated': recently_rated,
        'recent_comments': recent_comments,
        'newest_books': newest_books,
        'recently_rated': recently_rated,
        'recent_comments': recent_comments,
        'newest_books': newest_books,
        'best_rated_books': best_rated_books,
        'worst_rated_books': worst_rated_books,
    }

    if request.user.is_authenticated:
        relations = UserBookRelation.objects.filter(user=request.user)

        recently_read_ids = relations.filter(read=True).values_list('book_id', flat=True)[:5]
        to_read_ids = relations.filter(wishlist=True).values_list('book_id', flat=True)[:5]

        recently_read = Book.objects.filter(id__in=recently_read_ids).annotate(avg_rating=Avg('rating__stars'))
        to_read = Book.objects.filter(id__in=to_read_ids).annotate(avg_rating=Avg('rating__stars'))

        context['recently_read'] = recently_read
        context['to_read'] = to_read

    return render(request, 'home_authenticated.html' if request.user.is_authenticated else 'home.html', context)

def search(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # po registraci přesměrujeme na login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def import_books(request):
    if request.method == 'POST':
        form = ImportBooksForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            imported = 0
            for row in reader:
                Book.objects.get_or_create(
                    title=row['title'],
                    author=row['author'],
                    defaults={
                        'description': row.get('description', ''),
                        'genre': row.get('genre', ''),
                        'published_date': row.get('published_date') or None,
                    }
                )
                imported += 1
            messages.success(request, f'Importováno {imported} knih.')
            return redirect('book-list')
    else:
        form = ImportBooksForm()
    return render(request, 'books/import_books.html', {'form': form})

class BookDetailView(FormMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    form_class = RatingForm

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        if self.request.user.is_authenticated:
            relation = UserBookRelation.objects.filter(user=self.request.user, book=book).first()
            context['user_relation'] = relation

            user_rating = Rating.objects.filter(user=self.request.user, book=book).first()
            context['user_rating'] = user_rating

            if relation and relation.read:
                context['rating_form'] = RatingForm(instance=user_rating)
            else:
                context['rating_form'] = None
        else:
            context['rating_form'] = None
            context['user_rating'] = None

        context['ratings'] = Rating.objects.filter(book=book)
        context['average_rating'] = context['ratings'].aggregate(models.Avg('stars'))['stars__avg']
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')

        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                book=self.object,
                defaults={
                    'stars': form.cleaned_data['stars'],
                    'comment': form.cleaned_data['comment']
                }
            )
        return redirect('book-detail', pk=self.object.pk)

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'genre', 'published_date', 'cover_image']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

@login_required
def toggle_read(request, pk):
    book = get_object_or_404(Book, pk=pk)
    relation, created = UserBookRelation.objects.get_or_create(user=request.user, book=book)
    relation.read = not relation.read
    relation.save()
    return redirect('book-detail', pk=pk)

@login_required
def toggle_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    relation, created = UserBookRelation.objects.get_or_create(user=request.user, book=book)
    relation.wishlist = not relation.wishlist
    relation.save()
    return redirect('book-detail', pk=pk)

class ReadBooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list_read.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        user_books = UserBookRelation.objects.filter(user=self.request.user, read=True).values_list('book_id', flat=True)
        return Book.objects.filter(id__in=user_books).annotate(avg_rating=Avg('rating__stars'))


class WishlistBooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list_wishlist.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        user_books = UserBookRelation.objects.filter(user=self.request.user, wishlist=True).values_list('book_id', flat=True)
        return Book.objects.filter(id__in=user_books).annotate(avg_rating=Avg('rating__stars'))


class BestRatedBooksView(ListView):
    model = Book
    template_name = 'books/book_list_best.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('-avg_rating')


class WorstRatedBooksView(ListView):
    model = Book
    template_name = 'books/book_list_worst.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        return Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('avg_rating')

@login_required
def export_books(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="knihy.csv"'

    writer = csv.writer(response)
    response.write('\ufeff')

    writer.writerow(['title', 'author', 'description', 'genre', 'published_date', 'location'])

    for book in Book.objects.all():
        writer.writerow([
            book.title,
            book.author,
            book.genre,
            book.series,
            book.published_date.strftime('%Y-%m-%d') if book.published_date else '',
            book.location,
            book.description,
        ])

    return response

def about(request):
    return render(request, 'books/about.html')

def loans(request):
    return render(request, 'books/loans.html')

def reading_room(request):
    return render(request, 'books/reading_room.html')

def author_list(request):
    authors = Book.objects.values('author').annotate(book_count=Count('id')).order_by('author')
    return render(request, 'authors/author_list.html', {'authors': authors})

def books_by_author(request, author_name):
    books = Book.objects.filter(author=author_name).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'authors/books_by_author.html', {'books': books, 'author_name': author_name})

def genre_list(request):
    genres = Book.objects.values('genre').annotate(count=Count('id')).order_by('genre')
    return render(request, 'genres/genre_list.html', {'genres': genres})

def genre_detail(request, genre):
    books = Book.objects.filter(genre=genre)
    return render(request, 'genres/genre_detail.html', {'genre': genre, 'books': books})

@login_required
def wishlist_view(request):
    relations = UserBookRelation.objects.filter(user=request.user, wishlist=True)
    books = Book.objects.filter(id__in=relations.values_list('book_id', flat=True)).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'books/wishlist.html', {'books': books})

@login_required
def read_books(request):
    books = Book.objects.filter(userbookrelation__user=request.user, userbookrelation__read=True)
    return render(request, 'books/read_books.html', {'books': books})

@login_required
def my_library(request):
    relations = UserBookRelation.objects.filter(user=request.user).filter(
        Q(read=True) | Q(rating__isnull=False)
    )
    book_ids = relations.values_list('book_id', flat=True).distinct()

    books = Book.objects.filter(id__in=book_ids).annotate(avg_rating=Avg('rating__stars'))

    return render(request, 'books/my_library.html', {'books': books})

@login_required
def read_books_view(request):
    relations = UserBookRelation.objects.filter(user=request.user, read=True)
    books = Book.objects.filter(id__in=relations.values_list('book_id', flat=True)).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'books/read_books.html', {'books': books})
