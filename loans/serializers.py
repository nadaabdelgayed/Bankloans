from rest_framework import serializers
from .models import LoanApplication,FundApplication, Transaction


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ('user_id', 'loan_amount', 'loan_tenure','loan_application_status','loan_application_updated','loan_application_created','loan_application_id')
class LoanApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ('user_id', 'loan_amount', 'loan_tenure','loan_application_updated','loan_application_created')

class FundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundApplication
        fields = ('user_id', 'fund_amount','fund_application_updated','fund_application_created','fund_application_status','fund_application_id')

class FundApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundApplication
        fields = ('user_id', 'fund_amount','fund_application_updated','fund_application_created') 

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('transaction_id', 'transaction_created', 'transaction_updated', 'transaction_type', 'transaction_amount', 'transaction_user_id')