from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ApplicationStatus, BankBalance, FundApplication, Loan, LoanApplication, LoanParams, Transaction, TransactionType, UserTypes
from .serializers import  FundApplicationPostSerializer, FundApplicationSerializer, LoanApplicationPostSerializer, LoanApplicationSerializer, TransactionSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission,User, Group
# Create your views here.

class LoanApplicationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        if(request.data.get('loan_amount')==None or request.data.get('loan_tenure')==None):
            return Response(status=status.HTP_400_BAD_REQUEST, data={'error':'loan_amount and loan_tenure are required'})
        data = {
            'loan_amount': request.data.get('loan_amount'),
            'loan_tenure': request.data.get('loan_tenure'),
            'user_id': request.user.id,
        }
        bank_balance = BankBalance.objects.get(id=1)
        loan_params = LoanParams.objects.get(id=1)
        if(bank_balance.bank_balance < data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Insufficient Balance, please try again later or enter an amount less than bank balance: '+str(bank_balance.bank_balance) })
        if(loan_params.bank_min_loan > data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Loan Amount is less than minimum loan amount: '+str(loan_params.bank_min_loan) })
        if(loan_params.bank_max_loan < data['loan_amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Loan Amount is greater than maximum loan amount: '+str(loan_params.bank_max_loan) })
        serializer = LoanApplicationPostSerializer(data=data)
        print('data check passed')
        if serializer.is_valid():
            print('serializer is valid')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('serializer is not valid')
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        if(len(request.user.groups.all())==0 or(len(request.user.groups.all())>0 and request.user.groups.all()[0].name!="Customer")):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        ct=ContentType.objects.get_for_model(LoanApplication)
        loan_permission=Permission.objects.filter(content_type=ct)

        print([perm.codename for perm in loan_permission])
        loan_applications = LoanApplication.objects.filter(user_id=request.user.id)
        serializer = LoanApplicationSerializer(loan_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request,pk):

        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
       
        loan_application = LoanApplication.objects.get(pk=pk)
        if(loan_application.user_id != request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        loan_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FundApplicationApiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if(request.user.groups.all()[0].name=="Loan Provider"):
            if(request.data.get('fund_amount')==None):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'fund_amount is required'})
            data = {
            'fund_amount': request.data.get('fund_amount'),
            'user_id': request.user.id,
            }
            print(data)

            serializer = FundApplicationPostSerializer(data=data)
            print('data check passed')
            if serializer.is_valid():
                print('serializer is valid')
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('serializer is not valid')
            print(serializer.errors)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def get(self, request):
        fund_applications = FundApplication.objects.filter(user_id=request.user.id)
        serializer = FundApplicationSerializer(fund_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request,pk):
        fund_application = FundApplication.objects.get(pk=pk)
        if(fund_application.user_id != request.user.id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        fund_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    

class TransactionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        
        transactions = Transaction.objects.filter(transaction_user_id=request.user.id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        if(request.user.groups.all()[0].name!="Customer"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'You are not a customer'})
        if(request.data.get('transaction_amount')==None):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'Invalid data, please ensure that you have entered transaction_type and transaction_amount'})
        loans= Loan.objects.filter(loan_user_id=request.user.id)
        if(len(loans)==0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'No loans found'})
        count=0
        for loan in loans:
            if(loan.loan_status=="ongoing"):
                count+=1
        if(count==0):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'No ongoing loans found'})

                
        data = {
            'transaction_type': TransactionType.INSTALLMENTS.value,
            'transaction_amount': request.data.get('transaction_amount'),
            'transaction_user_id': request.user,
        }
        bankBal=BankBalance.objects.get(pk=1)
        bankBal.bank_balance+=request.data.get('transaction_amount')
        bankBal.save()
        Transaction.objects.create(**data)

        # serializer = TransactionSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(status=status.HTTP_201_CREATED)
  
class BankPersonnelFundApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Bank Personnel"):
            fund_applications = FundApplication.objects.filter(fund_application_status=ApplicationStatus.PENDING.value)
            fund_serializer = FundApplicationSerializer(fund_applications, many=True)
            return Response({'fund_applications':fund_serializer.data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            if(request.data.get("application_status"==None or request.data.get("id")==None)):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'please ensure all fields are filled:':'application_status, id'})
            bankBalance=BankBalance.objects.get(pk=1)
            appStatus=request.data.get('application_status')
            fund_application = FundApplication.objects.get(pk=request.data.get('id'))
            if(fund_application.fund_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'application status':'not pending'})
            fund_application.fund_application_status = appStatus
            if(fund_application.fund_application_status==ApplicationStatus.APPROVED.value):
                bankBalance.bank_balance+=fund_application.fund_amount
                Transaction.objects.create(transaction_type=TransactionType.FUND.value,transaction_amount=fund_application.fund_amount,transaction_user_id=fund_application.user_id)
                bankBalance.save()
            fund_application.save()
                    

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request,pk):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            fund_application = FundApplication.objects.get(pk=pk)
            if(fund_application.fund_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            fund_application.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    


class BankPersonnelLoanApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get(self, request):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Bank Personnel"):
            loan_applications = LoanApplication.objects.filter(loan_application_status=ApplicationStatus.PENDING.value)
            serializer = LoanApplicationSerializer(loan_applications, many=True)
            return Response({'loan_applications':serializer.data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            if(request.data.get("application_status"==None or request.data.get("id")==None or request.data.get("loan_interest_rate")==None)):
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'please ensure all fields are filled:':'application_status, id, loan_interest_rate'})
            bankBalance=BankBalance.objects.get(pk=1)
            appStatus=request.data.get('application_status')

            loan_application = LoanApplication.objects.get(pk=request.data.get('id'))
            if(loan_application.loan_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            loan_application.loan_application_status = appStatus
            
            
            if(loan_application.loan_application_status==ApplicationStatus.APPROVED.value):
                if(bankBalance.bank_balance<loan_application.loan_amount):
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'bank balance':'not enough'})
                bankBalance.bank_balance-=loan_application.loan_amount
                bankBalance.save()
                Loan.objects.create(loan_amount=loan_application.loan_amount,
                                    loan_user_id=loan_application.user_id,
                                    loan_interest=request.data.get('loan_interest_rate'),
                                    loan_tenure=loan_application.loan_tenure)
                Transaction.objects.create(transaction_type=TransactionType.LOAN.value,transaction_amount=loan_application.loan_amount,transaction_user_id=loan_application.user_id)
            # print(loan_application)
            loan_application.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def delete(self, request,pk):
        if(str(request.user.groups.all()[0])=="Bank Personnel"):
            loan_application = LoanApplication.objects.get(pk=pk)
            if(loan_application.loan_application_status!=ApplicationStatus.PENDING.value):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            loan_application.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
class AmortizationApiView(APIView):
    # only loan providers can access this class
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request,pk):
        if(len(request.user.groups.all())>0 and str(request.user.groups.all()[0])=="Loan Provider"):
            loan = Loan.objects.filter(loan_id=pk)
            if(len(loan)==0):
                return Response(status=status.HTTP_404_NOT_FOUND)
            loan=loan[0]
            AmortizationTable=[]
            for i in range(loan.loan_tenure):
                entry={
                    'month':i+1,
                    'payment':'{:.2f}'.format(loan.loan_amount/loan.loan_tenure+loan.loan_interest*loan.loan_amount/loan.loan_tenure),
                    'principal':loan.loan_amount/loan.loan_tenure,
                    'interest':loan.loan_interest*loan.loan_amount/loan.loan_tenure,
                    'balance':loan.loan_amount-(i+1)*loan.loan_amount/loan.loan_tenure,
                }
                AmortizationTable.append(entry)
            return Response({'amortization_table':AmortizationTable}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
