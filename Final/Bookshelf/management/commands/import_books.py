import csv
from django.core.management.base import BaseCommand
from bookshelf.models import Book
from datetime import datetime

class Command(BaseCommand):
    help = 'Import books from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        with open(kwargs['csv_file'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                book, created = Book.objects.get_or_create(
                    title=row['title'],
                    author=row['author'],
                    defaults={
                        'description': row.get('description', ''),
                        'genre': row.get('genre', ''),
                        'published_date': datetime.strptime(row['published_date'], '%Y-%m-%d').date() if row.get('published_date') else None,
                    }
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} books.'))