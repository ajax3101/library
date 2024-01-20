from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg
from matplotlib import pyplot as plt
import io
import urllib, base64
from django.http import JsonResponse
from plotly.offline import plot
import plotly.graph_objs as go
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
    authors_list = Author.objects.all()
    paginator = Paginator(authors_list, 10)  # 10 авторів на сторінці

    page = request.GET.get('page')
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, 'library_app/author_list.html', {'authors': authors})

def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'library_app/genre_list.html', {'genres': genres})

def statistics(request):
    # Статистика за жанрами
    genres_data = Book.objects.values('genre').annotate(count=Count('genre'))
    genres_labels = [data['genre'] for data in genres_data]
    genres_counts = [data['count'] for data in genres_data]

    # Статистика за авторами
    authors_data = Author.objects.annotate(count=Count('book'))
    authors_labels = [author.name for author in authors_data]
    authors_counts = [author.count for author in authors_data]

    # Статистика за прочитаними книгами
    read_books_count = Book.objects.filter(is_read=True).count()
    unread_books_count = Book.objects.filter(is_read=False).count()

    # Загальна статистика
    total_books_count = Book.objects.count()
    average_age = Book.objects.aggregate(avg_age=Avg('release_year'))

    # Створення графіків
    fig, ax = plt.subplots()
    ax.bar(genres_labels, genres_counts)
    ax.set_title('Статистика за жанрами')
    ax.set_xlabel('Жанр')
    ax.set_ylabel('Кількість книг')
    genres_img = io.BytesIO()
    plt.savefig(genres_img, format='png')
    genres_img.seek(0)
    genres_img_data = base64.b64encode(genres_img.getvalue()).decode()

    fig, ax = plt.subplots()
    ax.pie(authors_counts, labels=authors_labels, autopct='%1.1f%%')
    ax.set_title('Статистика за авторами')
    authors_img = io.BytesIO()
    plt.savefig(authors_img, format='png')
    authors_img.seek(0)
    authors_img_data = base64.b64encode(authors_img.getvalue()).decode()

    fig, ax = plt.subplots()
    ax.bar(['Прочитано', 'Залишилося'], [read_books_count, unread_books_count])
    ax.set_title('Статистика за прочитаними книгами')
    ax.set_ylabel('Кількість книг')
    read_books_img = io.BytesIO()
    plt.savefig(read_books_img, format='png')
    read_books_img.seek(0)
    read_books_img_data = base64.b64encode(read_books_img.getvalue()).decode()

    context = {
        'genres_img_data': genres_img_data,
        'authors_img_data': authors_img_data,
        'read_books_img_data': read_books_img_data,
        'total_books_count': total_books_count,
        'average_age': average_age['avg_age'],
    }

    return render(request, 'library_app/statistics.html', context)

def stats(request):
    return render(request, 'library_app/stats.html')

def update_genre_chart(request):
    genres_data = Book.objects.values('genre').annotate(count=Count('genre'))
    genres_labels = [data['genre'] for data in genres_data]
    genres_counts = [data['count'] for data in genres_data]

    genre_chart = go.Figure(data=[go.Bar(x=genres_labels, y=genres_counts)])
    genre_chart_html = plot(genre_chart, output_type='div', include_plotlyjs=False)

    return JsonResponse({'genre_chart_html': genre_chart_html})

def update_author_chart(request):
    authors_data = Author.objects.annotate(count=Count('book'))
    authors_labels = [author.name for author in authors_data]
    authors_counts = [author.count for author in authors_data]

    author_chart = go.Figure(data=[go.Pie(labels=authors_labels, values=authors_counts)])
    author_chart_html = plot(author_chart, output_type='div', include_plotlyjs=False)

    return JsonResponse({'author_chart_html': author_chart_html})
