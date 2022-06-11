from core.models import AccountStatusDeficit, Client
from rest_framework import serializers


class AccountStatusDeficitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatusDeficit
        fields = ['id', 'cvr', 'client', 'client_name', 'date', 'entry', 'period', 'balance', 'order', 'created_at',
                  'updated_at']

    def validate(self, attrs):
        accountStatusDeficit = AccountStatusDeficit.objects.filter(
            cvr__exact=attrs['cvr'],
            date__exact=attrs['date'],
            entry__exact=attrs['entry'],
            period__exact=attrs['period'],
            balance__exact=attrs['balance']
        )
        if accountStatusDeficit.exists():
            accountStatusDeficit.delete()
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class AccountStatusDeficitSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = AccountStatusDeficit
        fields = ['id', 'cvr', 'client', 'client_name', 'date', 'entry', 'period', 'balance', 'order', 'created_at',
                  'updated_at']
