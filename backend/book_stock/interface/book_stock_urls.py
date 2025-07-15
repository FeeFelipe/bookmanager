from django.urls import path

from .book_stock_view import BookStockView

urlpatterns = [
    path('', BookStockView.as_view()),
    path('<int:book_stock_id>/', BookStockView.as_view()),
]
