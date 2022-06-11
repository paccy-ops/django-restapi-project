from core.models import EIndkomst
from eindkomst import serializers, utils
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from eindkomst.total_amount import calculate_total_amount
from django.db.models import Q


# Create your views here.

class EIndkomstListCreateView(ListCreateAPIView):
    serializer_class = serializers.EindkomstSerializers
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=user)

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        eindkomst = EIndkomst.objects.all()
        if cvr_client:
            eindkomst = eindkomst.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        return eindkomst


class EIndkomstDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.EindkomstSerializersDetails
    permission_classes = [IsAuthenticated]
    queryset = EIndkomst.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset


class UniqueCvrAndClient(APIView):
    @staticmethod
    def get(request):
        cvr_client = request.query_params.get('cvr')
        data = []
        da = {}
        cvrs = set()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accountsStatus = EIndkomst.objects.all()
        if cvr_client:
            accountsStatus = accountsStatus.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        for a in accountsStatus:
            cvrs.add(a.cvr)
        for i in cvrs:
            accounts = EIndkomst.objects.filter(cvr=i)
            # for d in accounts:
            result_page = paginator.paginate_queryset(accounts, request)
            serializer = serializers.EindkomstSerializersDetails(result_page, many=True)
            for ids in range(len(serializer.data)):
                dat = {'cvr': serializer.data[ids]['cvr'], 'client_name': serializer.data[ids]['client_name']}
                data.append(dat)
        res_lists = []
        for i in range(len(data)):
            if data[i] not in data[i + 1:]:
                res_lists.append(data[i])
        return Response({"count": len(res_lists), "data": res_lists})


class OrderByMonthAndCvrAndClient(APIView):
    @staticmethod
    def get(request, cvr_pk):
        paginator = PageNumberPagination()
        paginator.page_size = 1
        res_list = []
        data = {}
        totals = {}
        years = EIndkomst.objects.filter(cvr__exact=cvr_pk).values_list('year', flat=True).order_by('-year').distinct(
            'year')

        for year in years:
            year_data = {}
            year_data['year'] = year
            year_data['data'] = {
                '1': [],
                '2': [],
                '3': [],
                '4': []
            }

            months = EIndkomst.objects.filter(cvr__exact=cvr_pk, year__exact=year).order_by('month')
            for month in months:
                month_period = {'Period': utils.get_period(month.month)}
                month_period.update(month.data)
                year_data['data'][str(month.quarter)].append(month_period)

                # get data for total
                for key in month.data.keys():
                    value = 0
                    if month.data[key]:
                        tokens = month.data[key].split(',')
                        whole = tokens[0].replace('.', '')
                        cents = tokens[1]
                        value = float(f'{whole}.{cents}')
                    if key not in totals.keys():
                        totals[key] = [value]
                    else:
                        totals[key].append(value)

                # compute for total
                if len(year_data['data'][str(month.quarter)]) >= 3:
                    for key in totals.keys():
                        _total = sum(totals[key])
                        totals[key] = utils.get_euro_format(_total)

                    quarter_total = {'Period': 'Total'}
                    quarter_total.update(totals)
                    year_data['data'][str(month.quarter)].append(quarter_total)
                    totals = {}

                if (len(months) - (list(months).index(month))) <= 2 and len(months) % 3 != 0:
                    totals = {}

            res_list.append(year_data)

        page = paginator.paginate_queryset(res_list, request)
        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(data)
