from django.shortcuts import render


def about(request):
    return render(request, 'books/about.html')


def reading_room(request):
    return render(request, 'books/reading_room.html')
