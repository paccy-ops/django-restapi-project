from rest_framework import serializers
from core.models import EIndkomst, Client


class EindkomstSerializers(serializers.ModelSerializer):
    class Meta:
        model = EIndkomst
        fields = "__all__"

    def validate(self, attrs):
        eindkomst = EIndkomst.objects.filter(
            cvr__exact=attrs['cvr'],
            year__exact=attrs['year'],
            month__exact=attrs['month'],
            quarter__exact=attrs['quarter']
        )
        if eindkomst.exists():
            eindkomst.delete()
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class EindkomstSerializersDetails(serializers.ModelSerializer):
    class Meta:
        model = EIndkomst
        fields = "__all__"


class EindkomstSerializersFormat(serializers.ModelSerializer):
    class Meta:
        model = EIndkomst
        fields = ['year', 'quarter', 'data']
