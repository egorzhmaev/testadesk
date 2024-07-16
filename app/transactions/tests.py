from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from .models import BankAccount, Operation

from .views import OperationAPIView


class GetPagesTestCase(TestCase):
    fixtures = ['db_test.json']

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_accounts_get(self):
        """Получает списки счетов и сравнивает"""
        w = list(BankAccount.objects.all().values())
        path = reverse('accounts')
        response = self.client.get(path)
        self.assertEqual(w, response.data)

    def test_account_balance(self):
        """Баланс счета на момент совершения операции"""
        account = Operation.objects.filter(id=18).values()
        balance = OperationAPIView()
        account_balance = list(balance.account_balance(account))[0]['account_balance']
        self.assertEqual(account_balance, 219.64)

    def test_new_operation_balance(self):
        """Обновление баланса при добавлении операции"""
        BankAccount.objects.create(name='Новый счет')
        response = self.client.post(reverse('transactions'),
                                    {'account': 6, 'date': '2024-01-01', 'amount': 100.00},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BankAccount.objects.get(id=6).balance, 100.00)

    def test_delete_operation_balance(self):
        """Обновление баланса при удалении операции"""
        self.assertEqual(float(BankAccount.objects.get(id=3).balance), 330.96)
        response = self.client.delete('/transactions/19')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(BankAccount.objects.get(id=3).balance), 219.64)

    def tearDown(self):
        "Действия после выполнения каждого теста"
