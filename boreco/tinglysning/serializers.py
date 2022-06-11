from core.models import Tinglysning, Client
from rest_framework import serializers


class TinglysningSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()

    class Meta:
        model = Tinglysning
        fields = [
            "id",
            'cvr',
            'client',
            'client_name',
            'client_responsible',
            'client_responsible_name',
            'tinglysning',
            'document_type',
            'role',
            'concern',
            'date_serial',
            'file_uploaded'
        ]

    def validate(self, attrs):
        tang = Tinglysning.objects.filter(
            cvr__exact=attrs['cvr'],
            tinglysning__exact=attrs['tinglysning'],
            document_type__exact=attrs['document_type'],
            role__exact=attrs['role'],
            concern__exact=attrs['concern'],
            date_serial__exact=attrs['date_serial']
        )

        if tang.exists():
            tang.delete()
        client = Client.objects.get(cvr__exact=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class TinglysningSerializerDetails(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()

    class Meta:
        model = Tinglysning
        fields = [
            "id",
            'cvr',
            'client',
            'client_name',
            'client_responsible',
            'client_responsible_name',
            'tinglysning',
            'document_type',
            'role',
            'concern',
            'date_serial',
            'file_uploaded'
        ]
