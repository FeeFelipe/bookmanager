from django.urls import path

from .book_view import BookView

urlpatterns = [
    path('', BookView.as_view()),
    path('<int:book_id>/', BookView.as_view()),
]
