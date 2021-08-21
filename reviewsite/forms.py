from django import forms
from django.forms import ModelForm
from .models import *


class Bookimageform(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['book_isbn', 'date_posted','author' ,'likes','dislikes']
    