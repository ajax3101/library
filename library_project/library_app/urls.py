from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from .views import book_list, add_book, profile_view, register_view, search_view, view_book, edit_book, delete_book, statistics, stats, update_genre_chart, update_author_chart
from . import views

app_name = 'library_app'


urlpatterns = [
    #path('', views.index, name="index"),
    path('', views.book_list, name='book_list'),
    path('books/', views.book_list, name='book_list'),
    path('authors/', views.author_list, name='author_list'),
    path('genres/', views.genre_list, name='genre_list'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:book_id>/', views.view_book, name='view_book'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('statistics/', statistics, name='statistics'),
    path('stats/', stats, name='stats'),
    path('update_genre_chart/', update_genre_chart, name='update_genre_chart'),
    path('update_author_chart/', update_author_chart, name='update_author_chart'),
    path('profile/', profile_view, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register_view'),
    path('search/', search_view, name='search_view'),
    #path('author/<int:author_id>/', views.view_author, name='view_author'),
    #path('genre/<int:genre_id>/', views.view_genre, name='view_genre'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)