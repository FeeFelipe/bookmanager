from django.urls import path

from .book_category_view import BookCategoryView

urlpatterns = [
    path('', BookCategoryView.as_view()),
    path('<int:book_category_id>/', BookCategoryView.as_view()),
]
