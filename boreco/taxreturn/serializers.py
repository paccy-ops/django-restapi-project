from core.models import TaxReturn
from rest_framework import serializers
from core.models import Client


class TaxReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxReturn
        fields = ['cvr',
                  'client',
                  'client_name',
                  'skatAmount',
                  'casewareAmount',
                  'identifier',
                  'filingStatus']

        def validate(self, attrs):
            client = Client.objects.get(cvr=attrs['cvr'])
            attrs['client'] = client
            attrs['client_name'] = client.client_name
            return attrs
