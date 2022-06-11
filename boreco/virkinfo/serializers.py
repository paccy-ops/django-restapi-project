from rest_framework import serializers
from core.models import Virkinfo, Client


class VirkInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Virkinfo
        fields = "__all__"

    def validate(self, attrs):
        client = Client.objects.get(cvr__exact=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class VirkInfoSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = Virkinfo
        fields = "__all__"
