# import numpy as np
# from cv2 import cv2
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from core.models import Tinglysning
from tinglysning import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from wsgiref.util import FileWrapper
from django.core.files.storage import default_storage as storage
from django.db.models import Q


class TinglysningListView(ListCreateAPIView):
    serializer_class = serializers.TinglysningSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Tinglysning.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        data['client_responsible_name'] = user.full_name
        return serializer.save(client_responsible=user)

    def get_queryset(self):
        cvr_client = self.request.query_params.get('cvr')
        tings = Tinglysning.objects.all()
        if cvr_client:
            tings = tings.filter(
                Q(cvr__icontains=cvr_client) | Q(client_name__icontains=cvr_client)
            )
        return tings
        


class TinglysningDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TinglysningSerializerDetails
    permission_classes = [IsAuthenticated]
    queryset = Tinglysning.objects.all()
    lookup_field = "cvr"

    def get_queryset(self):
        return self.queryset


class FileDownloadAPIView(APIView):
    @staticmethod
    def get(request, id, format=None):
        queryset = Tinglysning.objects.get(id=id)
        file_handle = queryset.file_uploaded.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/png')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.file_uploaded.name
        return response
