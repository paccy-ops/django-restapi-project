from core.models import VatCurrent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from vatCurrent import serializers


# Create your views here.

class VatCurrentViewList(ListCreateAPIView):
    """ List all AccountStatus, or create a new AccountStatus. """
    serializer_class = serializers.VatCurrentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = VatCurrent.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ['cvr', 'client_responsible_name', 'filing_deadline', 'period_start',
                        'period_end']

    search_fields = ['cvr', 'client_responsible_name', 'report_contact_name']

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=self.request.user)

    def get_queryset(self):
        return VatCurrent.objects.filter(client_responsible=self.request.user)


class VatCurrentViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatus instance."""
    serializer_class = serializers.VatCurrentSerializerDetails
    queryset = VatCurrent.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return self.queryset.filter(client_responsible=self.request.user)
