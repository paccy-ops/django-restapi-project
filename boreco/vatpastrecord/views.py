from core.models import VatPastRecord
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from vatpastrecord import serializers
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


# Create your views here.

class VatPastRecordViewList(ListCreateAPIView):
    """ List all Vat Past Record, or create a new Vat Past Record. """

    serializer_class = serializers.VatPastRecordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = VatPastRecord.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['filing_deadline', 'period_start',
                        'receipt_number', 'period_end', 'filing_date']


    def perform_create(self, serializer, **kwargs):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=self.request.user)


    def get_queryset(self):
        query_cvr = self.request.query_params.get('cvr')
        query_client_name = self.request.query_params.get('client_name')
        client_responsible_name = self.request.query_params.get('client_responsible_name')

        if query_cvr == None:
            query_cvr = ""

        if query_client_name == None:
            query_client_name = ""

        if client_responsible_name == None:
            client_responsible_name = ""

        vatpastrecord = VatPastRecord.objects.filter(cvr__icontains=query_cvr).filter(client_name__icontains=query_client_name).filter(
            client_responsible_name__icontains=client_responsible_name
        )

        return vatpastrecord


class VatPastRecordViewDetails(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a AccountStatus instance."""
    serializer_class = serializers.VatPastRecordSerializerDetails
    queryset = VatPastRecord.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(client_responsible=self.request.user)


class UniqueCvrAndClient(APIView):
    @staticmethod
    def get(request):

        cvr_client = request.query_params.get('client_name')

        data = {}
        paginator = PageNumberPagination()
        paginator.page_size = 10
        accounts = VatPastRecord.objects.order_by('cvr') \
            .distinct('cvr').values('cvr', 'client_name')

        if cvr_client:
            accounts = accounts.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            ) 

        page = paginator.paginate_queryset(accounts, request)

        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(data)
