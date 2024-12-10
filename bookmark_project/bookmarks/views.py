from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Bookmark
from django.contrib import messages
from .forms import SignupForm, BookmarkForm
from django.core.paginator import Paginator
import datetime

# User Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user data
            return redirect('login')  # Redirect to login page
    else:
        form = SignupForm()  # Show an empty signup form
    return render(request, 'bookmarks/signup.html', {'form': form})


# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Authenticate user
            login(request, user)  # Log in the user
            return redirect('bookmark_list')  # Redirect to the bookmark list
    else:
        form = AuthenticationForm()  # Show an empty login form
    return render(request, 'bookmarks/login.html', {'form': form})


# User Logout View
@login_required
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to login page



@login_required
def add_bookmark(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            # Check if the user already has 5 bookmarks
            bookmark_count = Bookmark.objects.filter(user=request.user).count()
            if bookmark_count >= 5:
                # Add error message and re-render the form
                messages.error(request, "Error: You already created 5 bookmarks.")
                return render(request, 'bookmarks/add_bookmark.html', {'form': form})

            # Save the bookmark if the limit is not exceeded
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
           
            return redirect('bookmark_list')
    else:
        form = BookmarkForm()

    # Render the form with errors or initially
    return render(request, 'bookmarks/add_bookmark.html', {'form': form})

# View all Bookmarks with Pagination and Search
@login_required
def bookmark_list(request):
    search_query = request.GET.get('search', '')  # Get search query from URL parameters
    bookmarks = Bookmark.objects.filter(user=request.user)  # Get all bookmarks for current user
    if search_query:
        bookmarks = bookmarks.filter(title__icontains=search_query)  # Filter bookmarks by title
    
    paginator = Paginator(bookmarks, 3)  # Paginate the bookmarks, 3 per page
    page_number = request.GET.get('page')  # Get page number from URL parameters
    page_obj = paginator.get_page(page_number)  # Get the current page of bookmarks

    return render(
        request, 
        'bookmarks/bookmark_list.html', 
        {'page_obj': page_obj, 'search_query': search_query}
    )



# Edit Bookmark View
@login_required
def edit_bookmark(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)  # Get the bookmark or 404 if not found
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)  # Fill form with existing bookmark data
        if form.is_valid():
            form.save()  # Save the edited bookmark
            return redirect('bookmark_list')  # Redirect to the bookmark list
    else:
        form = BookmarkForm(instance=bookmark)  # Show the form with existing bookmark data
    return render(request, 'bookmarks/add_bookmark.html', {'form': form})


# Delete Bookmark View
@login_required
def delete_bookmark(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)  # Get the bookmark or 404 if not found
    if request.method == 'POST':
        bookmark.delete()  # Delete the bookmark
        return redirect('bookmark_list')  # Redirect to the bookmark list
    return render(request, 'bookmarks/delete.html', {'bookmark': bookmark})  # Show confirmation page


# Search Bookmarks (JSON Response)
@login_required
def search_bookmarks(request):
    search_query = request.GET.get('search', '')  # Get search query from URL parameters
    bookmarks = Bookmark.objects.filter(user=request.user, title__icontains=search_query)  # Filter bookmarks

    # Prepare data for JSON response
    bookmark_data = [
        {
            "id": bookmark.id,
            "title": bookmark.title,
            "url": bookmark.url,
            "created_at": bookmark.created_at.strftime('%Y-%m-%d'),  # Format created_at date
        }
        for bookmark in bookmarks
    ]

    return JsonResponse({'bookmarks': bookmark_data})  # Return bookmarks in JSON format


def home(request):
    return render(request, 'bookmarks/home.html', {'current_year': datetime.datetime.now().year})