from core.models import Skattekonto
from rest_framework import serializers
from core.models import Client


class SerializerSkattekonto(serializers.ModelSerializer):
    class Meta:
        model = Skattekonto
        fields = "__all__"

    def validate(self, attrs):
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class SerializerSkattekontoDetails(serializers.ModelSerializer):
    class Meta:
        model = Skattekonto
        fields = "__all__"
