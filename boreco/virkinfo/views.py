from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.models import Virkinfo
from virkinfo.serializers import VirkInfoSerializer, VirkInfoSerializerDetails
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class VirkInfoViewList(ListCreateAPIView):
    """ List all VatAccountInfo, or create a new VatAccountInfo. """
    serializer_class = VirkInfoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Virkinfo.objects.all()

    def perform_create(self, serializer, **kwargs):
        return serializer.save()

    def get_queryset(self):
        return self.queryset


class VirkInfoViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a VatAccountInfo instance."""
    serializer_class = VirkInfoSerializerDetails
    queryset = Virkinfo.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return self.queryset
