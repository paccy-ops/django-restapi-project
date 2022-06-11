from core.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = ('cvr', 'client_name', 'created_at', 'updated_at')

    @staticmethod
    def get_created_at(obj):
        return obj.created_at

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at


class SerializerClients(serializers.Serializer):
    _id = serializers.CharField()
    company = serializers.CharField()
    cvr = serializers.CharField()
    version = serializers.IntegerField()
    scrape_date = serializers.DateTimeField()
