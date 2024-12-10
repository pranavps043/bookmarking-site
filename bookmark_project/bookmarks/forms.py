from django import forms
from .models import Bookmark
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm to handle user signup

# Signup Form for user registration
class SignupForm(UserCreationForm):
    class Meta:
        model = User  # Specify that this form will work with the User model
        fields = ['username', 'password1', 'password2']  # Fields for username, password1, and password2

# Bookmark Form for creating or editing bookmarks
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark  # Specify that this form will work with the Bookmark model
        fields = ['title', 'url']  # Fields for title and URL of the bookmark


