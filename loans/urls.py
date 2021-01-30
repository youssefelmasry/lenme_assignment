from django.urls import path
from loans.views import LoanSubmitView, OfferSubmitView

urlpatterns = [
    path('loan/submit/', LoanSubmitView.as_view()),
    path('offer/submit/<int:pk>/', OfferSubmitView.as_view()),
]
