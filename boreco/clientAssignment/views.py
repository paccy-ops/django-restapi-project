from clientAssignment import serializers
from core.models import ClientAssignment
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.


# class ClientAssignmentCreate(generics.CreateAPIView):
#     """create a Client Assignment View and get list of all client by a user"""
#     queryset = ClientAssignment.objects.all()
#     serializer_class = serializers.ClientAssignmentSerializer


class ClientAssignmentListView(ListCreateAPIView):
    # class ClientAssignmentListView(generics.ListAPIView):
    #     """create a Client Assignment View and get list of all client by a user"""
    #     queryset = ClientAssignment.objects.all()
    #     serializer_class = serializers.ClientAssignmentSerializer

    serializer_class = serializers.ClientAssignmentSerializer
    queryset = ClientAssignment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

    def get_queryset(self):
        return ClientAssignment.objects.filter(user_id=self.request.user)


# class ClientAssignmentDetailView(RetrieveUpdateDestroyAPIView):
class ClientAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientAssignment.objects.all()
    serializer_class = serializers.ClientAssignmentSerializerDetails
    # serializer_class = serializers.ClientAssignmentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return ClientAssignment.objects.filter(user_id=self.request.user)
