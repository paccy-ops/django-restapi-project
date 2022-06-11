from client import serializers
from core.data_from_mongo_db import MongoData
from core.models import Client
from core.mongodata import list_generator
from pymongo import MongoClient
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

client = MongoClient(
    'mongodb://divisor:0l6YIeoLMjL4yEpQ@104.40.187.114:27017/divisor?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
db = client['divisor']
client = db.get_collection('clients')
clients_data = client.find()

data_clients = set()
new_l = []
for x in clients_data:
    t = tuple(dict(x).items())
    if t not in data_clients:
        data_clients.add(t)
        new_l.append(dict(x))

for x in clients_data:
    t = tuple(dict(x).items())
    if t not in data_clients:
        data_clients.add(dict(x).get('company'))
        data_clients.add(dict(x).get('cvr'))
        new_l.append(t)

dataMongo = MongoData()


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def AllClientData(request):
#     try:
#         data_mango = dataMongo.get_client_data('clients', limit=20)
#         serializer_data = serializers.SerializerClients(data_mango, many=True)
#     except BaseException:
#         return Response("record not available")
#     return Response(serializer_data.data)


@api_view(['POST'])
def createClients(request):
    user = request.user
    for n in new_l:
        product = Client.objects.create(
            owner=user,
            client_name=f'{n[1][1]}',
            cvr=f'{n[2][1]}',
        )

        serializer = serializers.ClientSerializer(product, many=True)
        return Response(serializer.data)


class SaveData(GenericAPIView):
    serializer_class = serializers.ClientSerializer

    def post(self, request):
        for n in list_generator():
            if Client.objects.filter(cvr=n[1]).exists():
                continue
            request.data['client_name'] = n[0]
            # request.data['client_name'] = dict(n).get('company')
            # request.data['cvr'] = dict(n).get('cvr')
            request.data['cvr'] = n[1]
            serializer = self.serializer_class(data=request.data)

            serializer.is_valid(raise_exception=True)
            serializer.save(owner=self.request.user)

        msg = {'message': 'data loaded in database successful'}
        return Response(msg, status=status.HTTP_201_CREATED)


class ClientList(ListCreateAPIView):
    """create a client and get list of all client by a user"""

    serializer_class = serializers.ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ClientSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "cvr"

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)
