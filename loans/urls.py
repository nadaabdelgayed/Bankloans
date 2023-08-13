# from django.conf.urls import url
from django.urls import path, include
from .views import (AmortizationApiView, BankPersonnelFundApiView, BankPersonnelLoanApiView, FundApplicationApiView, LoanApplicationApiView, TransactionApiView)

urlpatterns = [
    path('loan-application/', LoanApplicationApiView.as_view()),
    path('loan-application/<int:pk>/', LoanApplicationApiView.as_view()),
    path('transaction/', TransactionApiView.as_view()),
    # path('transaction/<int:pk>/', TransactionApiView.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    path('fund-application/', FundApplicationApiView.as_view()),
    path('fund-application/<int:pk>/', FundApplicationApiView.as_view()),
    path('bank-panel-fund/', BankPersonnelFundApiView.as_view()),
    path('bank-panel/<int:pk>/', BankPersonnelFundApiView.as_view()),
    path('bank-panel-loan/', BankPersonnelLoanApiView.as_view()),
    path('bank-panel-loan/<int:pk>/', BankPersonnelLoanApiView.as_view()),
    path('amortization/<int:pk>/',  AmortizationApiView.as_view()),
    # path('bank-panel-loan/<int:pk>/', BankPersonnelLoanApiView.as_view()),

]