from django.db import models
from django.db.models import Manager


class BankAccount(models.Model):
    """Модель счёта"""
    name = models.CharField(max_length=130, blank=True, null=True, verbose_name="Название",
                            help_text="Название")
    balance = models.DecimalField(default=0.0, max_digits=12, decimal_places=2, verbose_name="Баланс",
                                  help_text="Текущий баланс на счете")
    objects = models.Manager()

    class Meta:
        db_table = 'bank_accounts'
        verbose_name = "Банковский счет"
        verbose_name_plural = "Банковские счета"

    def __str__(self):
        return self.name


class Operation(models.Model):
    """Модель операции"""
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE, related_name='operations',
                                verbose_name='Идентификатор счёта', help_text="Уникальный идентификатор")
    amount = models.DecimalField(default=0.0, max_digits=12, decimal_places=2, verbose_name="Сумма",
                                 help_text="Сумма транзакции")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата операции")

    objects: Manager = models.Manager()

    class Meta:
        db_table = 'operations'
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
