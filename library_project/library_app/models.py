from django.db import models



class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'
        ordering = ["name"]
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'
        ordering = ["name"]
    name = models.CharField(max_length=50, verbose_name = 'Заголовок')

    def __str__(self):
        return self.name

class Book(models.Model):
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ["title"]

    title = models.CharField(max_length=100, verbose_name = 'Заголовок')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name = 'Автор')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name = 'Жанр')
    release_year = models.PositiveIntegerField(verbose_name = 'Рік видання')
    is_read = models.BooleanField(default=False, verbose_name = 'Чек')
    img = models.ImageField(upload_to='book_images/', blank=True, null=True)

    def __str__(self):
        return self.title