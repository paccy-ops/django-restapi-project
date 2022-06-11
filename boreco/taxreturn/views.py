from core.models import TaxReturn
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from taxreturn import serializers
from django.db.models import Q


# Create your views here.

class TaxReturnListCreateView(ListCreateAPIView):
    serializer_class = serializers.TaxReturnSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        taxreturn = TaxReturn.objects.all()
        if cvr_client:
            taxreturn = taxreturn.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        return taxreturn


class TaxReturnDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaxReturnSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "cvr"

    def get_queryset(self):
        return TaxReturn.objects.all()
