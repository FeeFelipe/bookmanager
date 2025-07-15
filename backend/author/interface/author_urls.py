from django.urls import path

from .author_view import AuthorView

urlpatterns = [
    path('', AuthorView.as_view()),
    path('<int:author_id>/', AuthorView.as_view()),
]
