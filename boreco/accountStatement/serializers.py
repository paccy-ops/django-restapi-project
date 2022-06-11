from core.models import AccountStatement, Client
from rest_framework import serializers


class AccountStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = ['cvr', 'client', 'client_name', 'entry_date', 'entry_name', 'further_initiatives', 'amount', 'balance']

    def validate(self, attrs):
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class AccountStatementSerializeDetailsr(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = ['cvr', 'client', 'client_name', 'entry_date', 'entry_name', 'further_initiatives', 'amount', 'balance']
