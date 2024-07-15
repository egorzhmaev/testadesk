
from django.urls import path

from .views import BankAccountAPIView, OperationAPIView

urlpatterns = [
    path('accounts/', BankAccountAPIView.as_view(), name='accounts'),
    path('transactions/<int:id>', OperationAPIView.as_view()),
    path('transactions/', OperationAPIView.as_view()),
]
