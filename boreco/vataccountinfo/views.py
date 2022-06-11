from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from core.models import VatAccountInfo, AccountStatus, Virkinfo
from vataccountinfo.serializers import VatAccountInfoSerializer, VatAccountInfoSerializerDetails
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.utils import Util
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accountStatus import serializers
from core.models import VatCurrent

# Create your views here.


class VatAccountInfoViewList(ListCreateAPIView):
    """ List all VatAccountInfo, or create a new VatAccountInfo. """
    serializer_class = VatAccountInfoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = VatAccountInfo.objects.all()

    def perform_create(self, serializer, **kwargs):
        return serializer.save()

    def get_queryset(self):
        return self.queryset


class VatAccountInfoViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a VatAccountInfo instance."""
    serializer_class = VatAccountInfoSerializerDetails
    queryset = VatAccountInfo.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset


class AccountInfoForEmail(GenericAPIView):
    serializer_class = serializers.AccountStatusSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, cvr_pk):
        accountstatus = AccountStatus.objects.filter(cvr__exact=cvr_pk, order__exact=0)
        vatAccountInfo = VatAccountInfo.objects.get(cvr__exact=cvr_pk)
        vatCurrent = VatCurrent.objects.get(cvr__exact=cvr_pk)
        virkinfo = Virkinfo.objects.get(cvr__exact=cvr_pk)
        subject = "Account status"
        html_content = render_to_string("emails/invoice.html", {
            "accountstatus": accountstatus, "vatAccountInfo": vatAccountInfo, "virkinfo": virkinfo, "vatCurrent": vatCurrent
            }
        )
        text_content = strip_tags(html_content)
        email_data_to_send = {'subject': subject, 'body': text_content, 'to_email': virkinfo.email}
        Util.send_email_account_status(email_data_to_send, html_content)
        return Response({"message": f"message sent to {virkinfo.email}"})
