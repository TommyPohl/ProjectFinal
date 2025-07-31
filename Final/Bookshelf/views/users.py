from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from Bookshelf.models import Book

# Domovská stránka
def home(request):
    from Bookshelf.models import Book, Rating, UserBookRelation
    from django.db.models import Avg, Subquery, OuterRef, Q

    context = {}
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
        best_rated_books = Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        worst_rated_books = Book.objects.annotate(avg_rating=Avg('rating__stars')) \
            .filter(avg_rating__isnull=False).order_by('avg_rating')[:5]

        context.update({
            'best_rated_books': best_rated_books,
            'worst_rated_books': worst_rated_books,
        })

    return render(request, 'home_authenticated.html' if request.user.is_authenticated else 'home.html', context)


# Registrace nového uživatele
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})







