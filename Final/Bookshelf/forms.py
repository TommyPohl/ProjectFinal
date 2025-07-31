from django import forms
from .models import Book, Tag
from .models import Rating

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'description', 'genre',
            'series', 'published_date', 'location',
            'cover_image', 'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

class ImportBooksForm(forms.Form):
    csv_file = forms.FileField(label="CSV soubor")

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        labels = {
            'stars': 'Hodnocení (1–5)',
            'comment': 'Komentář',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['stars'].widget = forms.Select(choices=[(i, f"{i}★") for i in range(1, 6)])

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {'name': 'Název štítku'}

class BookTagForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Book
        fields = ['tags']