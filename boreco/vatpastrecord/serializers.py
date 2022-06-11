from core.models import VatPastRecord, User, Client
from rest_framework import serializers


class UsersListSerializerVat(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class VatPastRecordSerializer(serializers.ModelSerializer):
    client = serializers.CharField(read_only=True)
    client_name = serializers.CharField(read_only=True)
    client_responsible_name = serializers.CharField(read_only=True)
    client_responsible = UsersListSerializerVat(read_only=True)

    receipt = serializers.FileField()
    class Meta:
        model = VatPastRecord
        fields = [
            'id', 'cvr', 'client', 'client_name', 'period_start', 'period_end', 'receipt_number', 'receipt', 'filing_date', 'person_filing_vat',
            'person_cvr', 'client_address', 'email', 'output_vat', 'vat_goods_abroad', 'vat_services_abroad', 'input_vat',
            'oil_bottled_gas_vat', 'electricity_vat', 'natural_vat', 'coal_vat', 'co2_vat', 'water_vat', 'total_vat', 'order',
            'client_responsible', 'client_responsible_name', 'filing_deadline', 'status', 'indicating_type'
        ]

    @staticmethod
    def get_client(obj):
        return obj.client

    @staticmethod
    def get_client_name(obj):
        return obj.client_name

    @staticmethod
    def get_client_responsible_name(obj):
        return obj.client_responsible_name

    @staticmethod
    def get_client_responsible(obj):
        return obj.client_responsible

    def validate(self, attrs):
        # validating vat record before save
        client = Client.objects.get(cvr__exact=attrs['cvr'])
        vatpastrecord = VatPastRecord.objects.filter(cvr__exact=attrs['cvr'],
                                                     receipt_number__exact=attrs['receipt_number'],
                                                     period_end__exact=attrs['period_end'],
                                                     period_start__exact=attrs['period_start'])
        if vatpastrecord.exists():
            vatpastrecord.delete()
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class VatPastRecordSerializerDetails(serializers.ModelSerializer):
    receipt = serializers.FileField()
    
    class Meta:
        model = VatPastRecord
        fields = "__all__"
