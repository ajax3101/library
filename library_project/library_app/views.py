from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book,Genre,Author
from .forms import BookForm

# def index(request):
    # return render(request, 'library_app/index.html')
# def index(request):
#     books = Book.objects.all()
#     dict_obj = {'books':books,}
#     return render(request, 'library_app/index.html', dict_obj)
# def book_list(request):
#     books = Book.objects.all()
#     return render(request, 'library_app/book_list.html', {'books': books})
def book_list(request):
    sort_by = request.GET.get('sort', 'title')
    order = request.GET.get('order', 'asc')

    if order == 'asc':
        books = Book.objects.order_by(sort_by)
    else:
        books = Book.objects.order_by(f'-{sort_by}')

    paginator = Paginator(books, 20)  # Показывать 20 книг на каждой странице
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {'books': books}
    return render(request, 'library_app/book_list.html', context)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_app:book_list')
    else:
        form = BookForm()
    return render(request, 'library_app/add_book.html', {'form': form})

def view_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'library_app/view_book.html', {'book': book})

def edit_book(request, book_id):
    # Получаем объект книги из базы данных
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # Если форма была отправлена методом POST, обрабатываем данные формы
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_app:view_book', book_id=book_id)
    else:
        # Если это GET-запрос, инициализируем форму с текущими данными книги
        form = BookForm(instance=book)

    return render(request, 'library_app/edit_book.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    # Получаем книгу по идентификатору или возвращаем 404, если книга не найдена
    book = get_object_or_404(Book, pk=book_id)

    # Если запрос методом POST, значит пользователь подтвердил удаление
    if request.method == 'POST':
        # Удаляем книгу из базы данных
        book.delete()
        # Перенаправляем пользователя на список книг
        return redirect('library_app:book_list')

    # Если запрос методом GET, отображаем страницу подтверждения удаления
    return render(request, 'library_app/delete_book.html', {'book': book})

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library_app/author_list.html', {'authors': authors})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'library_app/genre_list.html', {'genres': genres})