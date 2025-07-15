from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/book/', include('book.interface.book_urls')),
    path('api/bookcategory/', include('book_category.interface.book_category_urls')),
    path('api/bookstock/', include('book_stock.interface.book_stock_urls')),
    path('api/author/', include('author.interface.author_urls')),
    path('api/branch/', include('branch.interface.branch_urls')),
]
