from core.models import Skattekonto
from Skattekonto import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q

# Create your views here.


class SkattekontoListCreateView(ListCreateAPIView):
    serializer_class = serializers.SerializerSkattekonto
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=user)

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        tings = Skattekonto.objects.all()
        if cvr_client:
            tings = tings.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        return tings


class SkattekontoDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SerializerSkattekontoDetails
    permission_classes = [IsAuthenticated]
    queryset = Skattekonto.objects.all()
    lookup_field = "cvr"

    def get_queryset(self):
        return self.queryset
