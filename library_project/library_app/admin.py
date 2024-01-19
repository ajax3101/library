from django.contrib import admin
from library_app.models import Book, Author, Genre

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     model = Book

#     # list_display = ()
#     list_per_page = 10
#     list_max_show_all = 100
