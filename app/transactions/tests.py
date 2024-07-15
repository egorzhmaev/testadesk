from django.test import TestCase

from django.urls import reverse

from .models import BankAccount


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

    def tearDown(self):
        "Действия после выполнения каждого теста"
