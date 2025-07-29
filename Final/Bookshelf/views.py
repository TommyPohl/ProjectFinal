from django.views.generic import ListView
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

class BookListView(ListView):
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'

def home(request):
    return render(request, 'home.html')

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