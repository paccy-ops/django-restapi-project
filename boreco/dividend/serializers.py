from core.models import Dividends, Client
from rest_framework import serializers
from utils.money_format import money_change_format


class DividendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividends
        fields = "__all__"

    def validate(self, attrs):
        if Dividends.objects.filter(cvr__exact=attrs['cvr']).exists():
            Dividends.objects.filter(cvr__exact=attrs['cvr']).delete()

        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        attrs['skat_total_dividend'] = (str(attrs['skat_total_dividend']))
        attrs['skat_recipient_vat'] = (str(attrs['skat_recipient_vat']))
        attrs['skat_recepient_tax'] = (str(attrs['skat_recepient_tax']))
        # attrs['caseware_total_dividend'] = (str(attrs['caseware_total_dividend']))
        attrs['skat_total_tax'] = (str(attrs['skat_total_tax']))
        return attrs


class DividendSerializerDetails(serializers.ModelSerializer):

    class Meta:
        model = Dividends
        fields = "__all__"
