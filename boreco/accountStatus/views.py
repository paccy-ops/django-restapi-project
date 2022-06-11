from accountStatus import serializers
from core.models import AccountStatus
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class AccountStatusViewList(ListCreateAPIView):
    """ List all AccountStatus, or create a new AccountStatus. """
    serializer_class = serializers.AccountStatusSerializer
    queryset = AccountStatus.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return AccountStatus.objects.all()


class AccountStatusViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatus instance."""
    serializer_class = serializers.AccountStatusSerializerDetails
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return AccountStatus.objects.all()


class AccountStatusList(GenericAPIView):
    serializer_class = serializers.AccountStatusSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        data = []
        cvrs = set()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountsStatus = AccountStatus.objects.all()
        for a in accountsStatus:
            cvrs.add(a.cvr)
        for cvr in cvrs:
            accounts = AccountStatus.objects.filter(cvr__exact=cvr)
            result_page = paginator.paginate_queryset(accounts, request)
            serializer = serializers.AccountStatusSerializer(result_page, many=True)
            da = {"cvr": cvr, "data": serializer.data}
            data.append(da)
        return paginator.get_paginated_response(data)
