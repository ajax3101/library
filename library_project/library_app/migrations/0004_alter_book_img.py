# Generated by Django 5.0.1 on 2024-01-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='book_images/'),
        ),
    ]