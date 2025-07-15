from django.urls import path

from .branch_view import BranchView

urlpatterns = [
    path('', BranchView.as_view()),
    path('<int:branch_id>/', BranchView.as_view()),
]
