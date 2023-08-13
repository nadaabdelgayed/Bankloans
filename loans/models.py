from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from enum import Enum
class UserTypes(Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    PROVIDER = 'provider'

class ApplicationStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class TransactionType(Enum):
    LOAN = 'loan'
    FUND = 'fund'
    INSTALLMENTS='installments'

class LoanStatus(Enum):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'



    # @classmethod
    # def choices(cls):
    #     return tuple((i.name, i.value) for i in cls)
    
# class User(models.Model):

#     user_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in UserTypes])

#     def __str__(self):
#         return self.user_name
    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_created = models.DateTimeField(auto_now_add=True)
    transaction_updated = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in TransactionType])
    transaction_amount = models.IntegerField()
    transaction_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_type
    
class BankBalance(models.Model):
    bank_balance = models.IntegerField()
    
class LoanParams(models.Model):
    bank_min_loan = models.IntegerField()
    bank_max_loan = models.IntegerField()


class FundApplication(models.Model):
    fund_application_id = models.AutoField(primary_key=True)
    fund_application_created = models.DateTimeField(auto_now_add=True)
    fund_application_updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fund_application_status = models.CharField(max_length=50, default=ApplicationStatus.PENDING.value,choices=[(tag.name, tag.value) for tag in ApplicationStatus])
    fund_amount = models.IntegerField()

    def __str__(self):
        return self.fund_application_status   
    


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    loan_created = models.DateTimeField(auto_now_add=True)
    loan_updated = models.DateTimeField(auto_now=True)
    loan_amount = models.IntegerField()
    loan_tenure = models.IntegerField()
    loan_interest = models.FloatField()
    loan_status = models.CharField(max_length=50, default=LoanStatus.ONGOING.value,choices=[(tag.name, tag.value) for tag in LoanStatus])
    loan_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.loan_status
    
class LoanApplication(models.Model):
    loan_application_id = models.AutoField(primary_key=True)
    loan_application_created = models.DateTimeField(auto_now_add=True)
    loan_application_updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_application_status = models.CharField(max_length=50, default=ApplicationStatus.PENDING.value,choices=[(tag.name, tag.value) for tag in ApplicationStatus])
    loan_amount = models.IntegerField()
    loan_tenure = models.IntegerField()

    def __str__(self):
        return self.loan_application_status  