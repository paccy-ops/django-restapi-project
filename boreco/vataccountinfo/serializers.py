from rest_framework import serializers
from core.models import VatAccountInfo, Client


class VatAccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatAccountInfo
        fields = "__all__"

    def validate(self, attrs):
        client = Client.objects.get(cvr__exact=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class VatAccountInfoSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = VatAccountInfo
        fields = "__all__"
