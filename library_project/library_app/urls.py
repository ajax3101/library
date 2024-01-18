from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path("admin/", admin.site.urls),
    #path('book/add/', views.add_book, name='add_book'),
    #path('book/<int:book_id>/', views.view_book, name='view_book'),
    #path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    #path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    #path('authors/', views.author_list, name='author_list'),
    #path('genres/', views.genre_list, name='genre_list'),
    #path('author/<int:author_id>/', views.view_author, name='view_author'),
    #path('genre/<int:genre_id>/', views.view_genre, name='view_genre'),
    
]
