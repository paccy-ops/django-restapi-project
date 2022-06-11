from core.models import ClientAssignment, Client
from rest_framework import serializers


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name']


class ClientAssignmentSerializer(serializers.ModelSerializer):
    client = ClientSerializers(many=False, read_only=True)

    class Meta:
        model = ClientAssignment
        fields = ['cvr', 'client', 'client_name', 'assignment', 'created_at', 'updated_at']

    def validate(self, attrs):
        client = Client.objects.get(cvr=attrs['cvr'])
        attrs['client'] = client
        attrs['client_name'] = client.client_name
        return attrs


class ClientAssignmentSerializerDetails(serializers.ModelSerializer):

    class Meta:
        model = ClientAssignment
        fields = ['cvr', 'client_name', 'assignment', 'updated_at']


# class ClientAssignmentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientAssignment
#         fields = ['cvr', 'client', 'assignment', 'created_at', 'updated_at']

# @staticmethod
# def get_client_info(obj):
#     return obj.client
# @staticmethod
# def get_client_name(obj):
#     return obj.client.client_name
