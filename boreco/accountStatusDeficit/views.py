from django.shortcuts import render
from accountStatusDeficit import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from core.models import AccountStatusDeficit, AccountStatusDeficitTotal
from django.db.models import Count
from django.db.models import Q


# Create your views here.

class AccountstatusDeficitUniqueCvr(APIView):
    @staticmethod
    def get(request):
        cvr_client = request.query_params.get('cvr')
        data = []
        cvrs = set()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountsStatus = AccountStatusDeficit.objects.all()
        if cvr_client:
            accountsStatus = accountsStatus.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        for a in accountsStatus:
            cvrs.add(a.cvr)
        for cvr in cvrs:
            accounts = AccountStatusDeficit.objects.filter(cvr__exact=cvr)
            da = {}
            result_page = paginator.paginate_queryset(accounts, request)
            serializer = serializers.AccountStatusDeficitSerializer(result_page, many=True)
            accountStatusDeficitTotal = AccountStatusDeficitTotal.objects.filter(cvr__exact=cvr)
            for df in range(len(serializer.data)):
                da['cvr'] = cvr
                da['client_name'] = serializer.data[df]['client_name']
                for a in accountStatusDeficitTotal:
                    da['ending_balance'] = a.total

            data.append(da)
        res_list = []
        for i in range(len(data)):
            if data[i] not in data[i + 1:]:
                res_list.append(data[i])
        return Response({"count": len(res_list), "data": res_list})

        # return paginator.get_paginated_response(data)


class OrderByOrderAccountstatusdeficit(APIView):
    @staticmethod
    def get(request, cvr_pk):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        eindkomst = AccountStatusDeficit.objects.filter(cvr__exact=cvr_pk).order_by('-order')
        result_page = paginator.paginate_queryset(eindkomst, request)
        serializer = serializers.AccountStatusDeficitSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AccountStatusDeficitViewList(ListCreateAPIView):
    """ List all AccountStatusDeficit, or create a new AccountStatusDeficit. """
    serializer_class = serializers.AccountStatusDeficitSerializer
    queryset = AccountStatusDeficit.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return AccountStatusDeficit.objects.all()


class AccountStatusDeficitViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatusDeficit instance."""
    serializer_class = serializers.AccountStatusDeficitSerializerDetails
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        accountStatusDeficit = AccountStatusDeficit.objects.all()
        if cvr_client:
            accountStatusDeficit = accountStatusDeficit.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client))
        return accountStatusDeficit


class AccountStatusDeficitList(GenericAPIView):
    serializer_class = serializers.AccountStatusDeficitSerializer
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        data = []
        cvrs = set()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountsStatus = AccountStatusDeficit.objects.all()
        for a in accountsStatus:
            cvrs.add(a.cvr)
        for cvr in cvrs:
            accounts = AccountStatusDeficit.objects.filter(cvr__exact=cvr)
            result_page = paginator.paginate_queryset(accounts, request)
            serializer = serializers.AccountStatusDeficitSerializer(result_page, many=True)
            da = {"cvr": cvr, "data": serializer.data}
            data.append(da)
        return paginator.get_paginated_response(data)
