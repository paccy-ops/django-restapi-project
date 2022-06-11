from django.shortcuts import render
from accountStatusDeficitTotal import serializers
from core.models import AccountStatusDeficitTotal
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# Create your views here.

class AccountDeficitTotalViewList(ListCreateAPIView):
    """ List all AccountStatusDeficitTotal, or create a new AccountStatusDeficitTotal. """
    serializer_class = serializers.AccountStatusDeficitTotalSerializer
    queryset = AccountStatusDeficitTotal.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        accountStatus = AccountStatusDeficitTotal.objects.all()
        if cvr_client:
            accountStatus = accountStatus.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client))
        return accountStatus


class AccountStatusDeficitTotalViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatusDeficitTotal instance."""
    serializer_class = serializers.AccountStatusDeficitTotalSerializerDetails
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return AccountStatusDeficitTotal.objects.all()


class AccountStatusDeficitTotalList(GenericAPIView):
    serializer_class = serializers.AccountStatusDeficitTotalSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        data = []
        cvrs = set()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountsStatus = AccountStatusDeficitTotal.objects.all()
        for a in accountsStatus:
            cvrs.add(a.cvr)
        for cvr in cvrs:
            accounts = AccountStatusDeficitTotal.objects.filter(cvr__exact=cvr)
            result_page = paginator.paginate_queryset(accounts, request)
            serializer = serializers.AccountStatusDeficitTotalSerializer(result_page, many=True)
            da = {"cvr": cvr, "data": serializer.data}
            data.append(da)
        return paginator.get_paginated_response(data)


class AccountstatusDeficitTotalByCvr(APIView):
    @staticmethod
    def get(request, cvr_pk):
        data = {}
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountstatusdeficittotal = AccountStatusDeficitTotal.objects.filter(cvr__exact=cvr_pk)
        for account in accountstatusdeficittotal:
            result_page = paginator.paginate_queryset(accountstatusdeficittotal, request)
            serializer = serializers.AccountStatusDeficitTotalSerializer(result_page, many=True)
            data['cvr'] = account.cvr
            data['data'] = serializer.data
            # data = {'cvr': account.cvr, 'data': serializer.data}
        return paginator.get_paginated_response(data)
