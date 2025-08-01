from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from Bookshelf.models import Tag

from ..models import Book, UserBookRelation, Rating
from ..forms import BookForm, ImportBooksForm
from ..forms import RatingForm, BookTagForm

import csv
from io import TextIOWrapper
from django.urls import reverse

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
        tag = self.request.GET.get('tag')

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
        if tag:
            queryset = queryset.filter(tags__name__iexact=tag)

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
        context['sort_by'] = self.request.GET.get('sort', '')
        context['filters'] = {
            'author': self.request.GET.get('author', ''),
            'genre': self.request.GET.get('genre', ''),
            'series': self.request.GET.get('series', ''),
            'location': self.request.GET.get('location', ''),
            'tag': self.request.GET.get('tag', ''),
        }
        return context

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            form.save_m2m()
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

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    average_rating = Rating.objects.filter(book=book).aggregate(Avg('stars'))['stars__avg']
    ratings = Rating.objects.filter(book=book).order_by('-created_at')

    user_rating = None
    rating_form = None
    tag_form = BookTagForm(instance=book)

    if request.user.is_authenticated:
        # ⭐ Hodnocení
        user_rating = Rating.objects.filter(book=book, user=request.user).first()
        if request.method == 'POST':
            rating_form = RatingForm(request.POST, instance=user_rating)
            if rating_form.is_valid():
                new_rating = rating_form.save(commit=False)
                new_rating.user = request.user
                new_rating.book = book
                new_rating.save()
                return redirect('book-detail', pk=book.pk)

            elif 'update_tags' in request.POST:
                tag_form = BookTagForm(request.POST, instance=book)
                if tag_form.is_valid():
                    tag_form.save()
                    return redirect('book-detail', pk=book.pk)
        else:
            rating_form = RatingForm(instance=user_rating)

    return render(request, 'books/book_detail.html', {
        'book': book,
        'ratings': ratings,
        'average_rating': average_rating,
        'user_rating': user_rating,
        'rating_form': rating_form,
        'tag_form': tag_form,
    })


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        if hasattr(form, 'save_m2m'):
            form.save_m2m()
        return response


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')



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

class ReadBooksListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list_read.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        user_books = UserBookRelation.objects.filter(user=self.request.user, read=True).values_list('book_id', flat=True)
        return Book.objects.filter(id__in=user_books).annotate(avg_rating=Avg('rating__stars'))

@login_required
def read_books_view(request):
    relations = UserBookRelation.objects.filter(user=request.user, read=True)
    books = Book.objects.filter(id__in=relations.values_list('book_id', flat=True)).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'books/read_books.html', {'books': books})

@login_required
def my_library(request):
    read_ids = UserBookRelation.objects.filter(user=request.user, read=True).values_list('book_id', flat=True)
    rated_ids = Rating.objects.filter(user=request.user).values_list('book_id', flat=True)

    book_ids = set(read_ids).union(rated_ids)

    books = Book.objects.filter(id__in=book_ids).annotate(avg_rating=Avg('rating__stars'))

    return render(request, 'books/my_library.html', {'books': books})

@login_required
def wishlist_view(request):
    relations = UserBookRelation.objects.filter(user=request.user, wishlist=True)
    books = Book.objects.filter(id__in=relations.values_list('book_id', flat=True)).annotate(avg_rating=Avg('rating__stars'))
    return render(request, 'books/wishlist.html', {'books': books})