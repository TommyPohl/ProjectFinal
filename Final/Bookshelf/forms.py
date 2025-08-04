from .models import Book, Tag
from .models import Rating
from django import forms
from .models import Loan

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
        # Přidání třídy CSS pro všechna formulářová pole
        self.fields['title'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['author'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['description'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['series'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['location'].widget.attrs.update({'class': 'form-control custom-width'})

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = ""

class BookTagForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Book
        fields = ['tags']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['book', 'borrower_name', 'contact', 'loan_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['borrower_name'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['contact'].widget.attrs.update({'class': 'form-control custom-width'})
        self.fields['loan_date'].widget.attrs.update({'class': 'form-control custom-width'})