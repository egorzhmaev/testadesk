import ast
from datetime import timedelta

from django.db.models import Q, Sum
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from dateutil import parser
from .models import BankAccount, Operation
from .serializers import BankAccountSerializer, OperationSerializer


class BankAccountAPIView(APIView):

    def get(self, request):
        """Возвращает все счета"""
        account = BankAccount.objects.all().values()
        return Response(list(account))

    def post(self, request):
        """Создаёт новый счёт"""
        account_new = BankAccount.objects.create(
            name=request.data['name']
        )

        return Response(BankAccountSerializer(account_new).data)


class OperationAPIView(APIView):

    def account_balance(self, account):
        """Баланс счета на момент совершения операции"""
        for i in account:
            amount = Operation.objects.filter(
                account_id=i['account_id'],
                date__lte=i['date'] + timedelta(days=1)
            ).aggregate(Sum('amount'))['amount__sum']
            i['account_balance'] = amount

        return account

    def get(self, request):
        """Возвращает все операции по заданным параметрам"""

        q = Q()
        if 'amount_from' in request.data:
            q &= Q(amount__gte=request.data['amount_from'])
        if 'amount_to' in request.data:
            q &= Q(amount__lte=request.data['amount_to'])
        if 'date_from' in request.data:
            q &= Q(date__gte=request.data['date_from'])
        if 'date_to' in request.data:
            q &= Q(date__lte=parser.parse(request.data['date_to']) + timedelta(days=1))
        if 'accounts' in request.data:
            q &= Q(account__in=ast.literal_eval(request.data['accounts']))
        if not request.data:
            account_get = Operation.objects.all().values()
            return Response(list(self.account_balance(account_get)))

        account = Operation.objects.filter(q).values()

        return Response(list(self.account_balance(account)))

    def post(self, request):
        """Создание новой операции"""
        operation = Operation.objects.create(
            account_id=request.data['account'],
            date=request.data['date'],
            amount=request.data['amount']
        )
        old_balance = BankAccount.objects.get(id=request.data['account']).balance
        account = BankAccount.objects.filter(id=request.data['account'])
        account.update(balance=int(old_balance) + int(request.data['amount']))

        return Response(OperationSerializer(operation).data)

    def delete(self, request, id):
        """Удаление операции"""
        operation = get_object_or_404(Operation.objects.all(), id=id)

        old_balance = Operation.objects.get(id=id).account.balance
        account_update = BankAccount.objects.filter(name=operation.account)
        account_update.update(balance=int(old_balance) - int(operation.amount))

        operation.delete()

        return Response()
