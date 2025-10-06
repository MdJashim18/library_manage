from django import forms
from .models import Book,BorrowRequest



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['name', 'registration_number', 'mobile', 'department']