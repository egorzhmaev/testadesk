from rest_framework import serializers

from .models import BankAccount, Operation


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['name', 'balance']


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'account_id', 'date', 'amount']

