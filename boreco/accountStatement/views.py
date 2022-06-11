from accountStatement import serializers
from core.models import AccountStatement
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class AccountStatementViewList(ListCreateAPIView):
    """ List all AccountStatus, or create a new AccountStatus. """
    serializer_class = serializers.AccountStatementSerializer
    queryset = AccountStatement.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return AccountStatement.objects.all()


class AccountStatementViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatus instance."""
    serializer_class = serializers.AccountStatementSerializeDetailsr
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return AccountStatement.objects.all()
