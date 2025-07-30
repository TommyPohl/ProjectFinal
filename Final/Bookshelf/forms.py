from django import forms
from .models import Book
from .models import Rating

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'series', 'published_date', 'location', 'cover_image', 'description']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ImportBooksForm(forms.Form):
    csv_file = forms.FileField(label="CSV soubor")

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }