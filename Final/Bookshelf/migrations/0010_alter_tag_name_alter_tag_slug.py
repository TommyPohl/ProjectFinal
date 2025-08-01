# Generated by Django 5.2.4 on 2025-07-31 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookshelf', '0009_alter_book_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
