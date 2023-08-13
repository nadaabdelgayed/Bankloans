from django.contrib import admin

# Register your models here.
from .models import  BankBalance, FundApplication, Loan, LoanApplication, Transaction,LoanParams

# admin.site.register(User)
admin.site.register(Loan)
admin.site.register(LoanApplication)
admin.site.register(Transaction)
admin.site.register(FundApplication)
admin.site.register(LoanParams)

admin.site.register(BankBalance)

