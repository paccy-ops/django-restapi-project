from core.models import AccountStatus, Client, AccountStatusDeficitTotal
from rest_framework import serializers


class AccountStatusDeficitTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatusDeficitTotal
        fields = ['id', 'cvr', 'total', 'created_at', 'updated_at']

    def validate(self, attrs):
        accountStatusDeficitTotal = AccountStatusDeficitTotal.objects.filter(
            cvr__exact=attrs['cvr'],
            total__exact=attrs['total']
        )
        if accountStatusDeficitTotal.exists():
            accountStatusDeficitTotal.delete()
        return attrs


class AccountStatusDeficitTotalSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = AccountStatusDeficitTotal
        fields = ['id', 'cvr', 'total', 'created_at', 'updated_at']
