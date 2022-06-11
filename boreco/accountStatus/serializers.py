from core.models import AccountStatus, Client
from rest_framework import serializers


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatus
        fields = ['id', 'cvr', 'client', 'client_name', 'status', 'amount', 'balance', 'order', 'period_date',
                  'created_at',
                  'updated_at']

    def validate(self, attrs):
        accountStatus = AccountStatus.objects.filter(
            cvr__exact=attrs['cvr'],
            period_date__exact=attrs['period_date'],
            balance__exact=attrs['balance'],
            status__exact=attrs['status'],
            amount__exact=attrs['amount']
        )
        if accountStatus.exists():
            accountStatus.delete()
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class AccountStatusSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = AccountStatus
        fields = ['id', 'cvr', 'client', 'client_name', 'status', 'amount', 'balance', 'order', 'period_date',
                  'created_at',
                  'updated_at']
