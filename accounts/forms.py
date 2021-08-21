from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


class CreateUserForm(UserCreationForm):
  group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
  class Meta:
    model = User
    fields = ['username', 'email', 'group', 'password1', 'password2']


