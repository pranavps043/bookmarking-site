from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_bookmark, name='add_bookmark'),
    path('', views.home, name='home'),  # Home page URL
    path('bookmark_list/', views.bookmark_list, name='bookmark_list'),
    path('<int:pk>/edit/', views.edit_bookmark, name='edit_bookmark'),
    path('<int:pk>/delete/', views.delete_bookmark, name='delete_bookmark'),
    path('search-bookmarks/', views.search_bookmarks, name='search_bookmarks'),
   
  
]
