from core.models import VatCurrent, User, Client
from rest_framework import serializers


class UsersListSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class VatClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['cvr', 'client_name']


class VatCurrentSerializer(serializers.ModelSerializer):

    class Meta:
        model = VatCurrent
        fields = [
            'cvr',
            'client',
            'client_name',
            'period_start',
            'period_end',
            'filing_deadline',
            'client_responsible',
            'report_contact_name',
            'report_contact_phone',
            'report_contact_email',
            'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        if VatCurrent.objects.filter(cvr__exact=attrs['cvr']).exists():
            VatCurrent.objects.get(cvr__exact=attrs['cvr']).delete()
        client = Client.objects.get(cvr__exact=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class VatCurrentSerializerDetails(serializers.ModelSerializer):

    class Meta:
        model = VatCurrent
        fields = [
            'cvr',
            'client',
            'client_name',
            'period_start',
            'period_end',
            'filing_deadline',
            'client_responsible',
            'report_contact_name',
            'report_contact_phone',
            'report_contact_email',
            'created_at',
            'updated_at'
        ]
