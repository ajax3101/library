from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'release_year', 'is_read']

# class BookSearchForm(forms.Form):
#     q = forms.CharField(label='Пошук', required=False)

