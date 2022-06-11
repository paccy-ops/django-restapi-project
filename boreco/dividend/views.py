from core.models import Dividends
from dividend import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q


# Create your views here.


class DividendViewList(ListCreateAPIView):
    """
    List all Dividend, or create a new Dividend.
    """
    serializer_class = serializers.DividendSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Dividends.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=user)

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        devidend = Dividends.objects.all()
        if cvr_client:
            devidend = devidend.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        return devidend


class DividendViewDetails(RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a Dividend instance.
        """
    serializer_class = serializers.DividendSerializerDetails
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return Dividends.objects.all()
