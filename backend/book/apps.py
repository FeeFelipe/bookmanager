from django.apps import AppConfig


class BookConfig(AppConfig):
    name = 'book'

    def ready(self):
        from book.application.task import create_book_task
